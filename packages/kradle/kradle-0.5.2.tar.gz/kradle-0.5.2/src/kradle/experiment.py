"""
Experiment runner for Kradle challenges.

An experiment is a collection of multiple runs of the same challenge and same agent(s).

Used for evaluating the performance of agents over several runs. 
"""

import time
import concurrent.futures 
from typing import List, Dict, Any, Optional
from kradle.api.client import KradleAPI
from kradle.api.resources import ChallengeParticipant
from kradle.models import Run, ExperimentResult, ExperimentParticipantResult
from kradle.logger import KradleLogger

class Experiment:
    """
    A class to run experiments with Kradle challenges.
    
    This class handles creating runs, monitoring their progress, and fetching logs from the run.
    """
    def __init__(
        self,              
        challenge_slug: str,
        participants: List[ChallengeParticipant],
        api_client: Optional[KradleAPI] = None,
        fetch_run_logs: Optional[bool] = True
    ):
        """
        Initialize the experiment runner.
        
        Args:
            challenge_slug: The slug identifier for the challenge
            participants: List of participants, each with agent name and optional role
            api_client: Optional API client for Kradle. If not provided, will use environment variable
            fetch_run_logs: Whether to fetch logs after each run. Default is True, set to False to disable for performance
        """
        self.challenge_slug = challenge_slug
        self.participants = participants
        self._internal_api_client = api_client or KradleAPI()
        self._logger = KradleLogger()
        self._fetch_run_logs = fetch_run_logs

        self.runs: Dict[str, Run] = {} # keyed by run id
        self.logs: Dict[str, List[Dict]] = {} # keyed by run id

        # do some sanity checks on challenge slug
        challenge = self._internal_api_client.challenges.get(self.challenge_slug)
        if not challenge['slug'] == self.challenge_slug:
            raise ValueError(f"Challenge slug {self.challenge_slug} does not match challenge slug in API response {challenge['slug']}")
        
        # do some sanity checks on participants
        for participant in self.participants:
            participant_response = self._internal_api_client.agents.get(participant['agent'])
            if not participant_response['username']:
                raise ValueError(f"Participant agent username not found in API response")
        
    def evaluate(self, 
        num_runs: int = 1,
        num_concurrent_runs: int = 1
    ) -> ExperimentResult:
        """
        Executes an experiment with the specified challenge and participants.
        
        Args:
            num_runs: Number of runs to create and execute (default: 1)
            num_concurrent_runs: Number of runs to execute concurrently (default: 1)
        
        Returns:
            ExperimentResult
        """
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent_runs) as executor:
            futures = []

            for _run_idx in range(num_runs):
                futures.append(executor.submit(self._create_and_monitor_run, _run_idx))
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    run = future.result()
                    print(f"Run {run.id} finished with status: {run.status}") if run else None
                except Exception as e:
                    print(f"Error when creating and monitoring run in future: {e}")
    
        finished_runs = [run for run in self.runs.values() if run.status == "finished"]
        results: Dict[str, ExperimentParticipantResult] = {}

        for run in finished_runs:
            for participant_id in run.participant_results:
                participant_result = run.participant_results[participant_id]
                if participant_id not in results:
                    results[participant_id] = ExperimentParticipantResult(
                        agent=participant_result.agent,
                        num_runs_finished=0,
                        win_count=0,
                        total_score=0,
                        average_score=0,
                        times_to_success=[],
                        average_time_to_success=0
                    )
                results[participant_id].num_runs_finished += 1
                results[participant_id].total_score += participant_result.score or 0
                results[participant_id].average_score = results[participant_id].total_score / results[participant_id].num_runs_finished
                
                if participant_result.winner:
                    results[participant_id].win_count += 1
                    results[participant_id].times_to_success.append(participant_result.time_to_success)
                    results[participant_id].average_time_to_success = sum(results[participant_id].times_to_success) / len(results[participant_id].times_to_success)

        duration = time.time() - start_time
        return ExperimentResult(
            num_runs=num_runs,
            num_runs_finished=len(finished_runs),
            results=results, # keyed by participant id to ExperimentParticipantResult
            runs=list(self.runs.values()),
            logs=self.logs,
            duration=duration
        )
    
    def _create_and_monitor_run(self, run_idx: int, max_retries: int = 3) -> Run:
        run_id = None
        run = None

        num_retries = 0
        while num_retries < max_retries:
            try:
                run_api_response = self._internal_api_client.runs.create(
                    challenge_slug=self.challenge_slug,
                    participants=self.participants
                )
                if run_api_response.get('runIds'):
                    run_id = run_api_response.get('runIds')[0]
                    
                if run_id:
                    run_api_response = self._internal_api_client.runs.get(run_id)
                    run = Run.from_api_response(run_api_response)
                    if run.id == run_id:
                        self.runs[run_id] = run
                        self._logger.log_info(f"Run #{run_idx} created successfully with id: {run_id}")
                        break
                    else:
                        self._logger.log_error(f"Error creating run #{run_idx}: run id not expected")
                else:
                    self._logger.log_error(f"Error creating run #{run_idx}: no run id returned")
            except Exception as e:
                self._logger.log_error(f"Error creating run #{run_idx}: {str(e)}")
                num_retries += 1
                if num_retries >= max_retries:
                    raise e
        
        if run_id:
            run = self._monitor_run(run_idx, run_id, poll_interval=1)
            self._logger.log_info(f"Run #{run_idx} id {run_id} ended with status: {run.status} { run.finished_status if run.finished_status else ''}")
            self.runs[run_id] = run

            if self._fetch_run_logs:
                self.logs[run_id] = self._internal_api_client.logs.dump(run_id)
        
        return run

    def _monitor_run(self, 
                    run_idx: int,
                    run_id: str, 
                    poll_interval: int = 1, 
                    max_retries: int = 3) -> Dict[str, Any]:
        """Monitor a run until it finishes or times out."""
        run = None

        run_status = ""
        num_retries = 0
        while True:
            # Get run status
            try:
                run_api_response = self._internal_api_client.runs.get(run_id)
                run = Run.from_api_response(run_api_response)

                if run_status != run.status:
                    # only log the run if the status has changed
                    run_status = run.status
                    self._logger.log_info(f"Run #{run_idx} id: {run_id} status: {run_status} (elapsed: {'0' if not run.total_time else f'{run.total_time/1000:.1f}s'})")
                    self.runs[run_id] = run
                
                # If the run is finished, break out of the loop
                if run_status == "finished":
                    break
                elif run_status == "failed" or run_status == "error":
                    self._logger.log_error(f"Run #{run_idx} id: {run_id} errored or failed!")
                    self._logger.log_error(run)
                    break
            except Exception as e:
                self._logger.log_error(f"Error monitoring run #{run_idx} id: {run_id}: {str(e)}")
                num_retries += 1
                if num_retries > max_retries:
                    self._logger.log_error(f"Run #{run_idx} id: {run_id} failed after max retries ({max_retries})")
                    break
                
            # Wait before polling again
            time.sleep(poll_interval)
        return run
    
    def fetch_run_logs(self) -> Dict[str, List[Dict]]:
        """Dumps all logs for all runs."""
        for run_id in self.runs.keys():
            self.logs[run_id] = self._internal_api_client.logs.dump(run_id)
        return self.logs
