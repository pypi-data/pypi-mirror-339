import requests
from typing import Dict, List, Optional, Any, Union
from .models import (
    Resume,
    ResumeResponse,
    JobDetailsResponse,
    ZoomMeetingResponse,
    ResumeRewriteResponse,
    IndexesListResponse,
    IndexResponse,
    SearchResponse,
    JobMatchResult,
)


class BaseClient:
    """Base class for Jobrex API clients."""

    def __init__(self, api_key: str, base_url: str = "https://api.jobrex.ai"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Api-Key {api_key}"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()


class ResumesClient(BaseClient):
    """
    Client for interacting with the Jobrex API for resumes.
    """
    

    def parse_resume(self, file_path: str) -> ResumeResponse:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self._make_request('POST', 'v1/resumes/extract/', files=files)

    def tailor_resume(self, user_data: Resume, job_details: Dict, sections: List[str]) -> Resume:
        data = {
            "user_data": user_data,
            "job_details": job_details,
            "sections": sections
        }
        return self._make_request('POST', 'v1/resumes/tailor/', json=data)

    def rewrite_resume_section(self, text: str, section_type: Optional[str] = "") -> ResumeRewriteResponse:
        data = {
            "text": text,
            "type": section_type
        }
        return self._make_request('POST', 'v1/resumes/rewrite/', json=data)

    def list_resume_indexes(self) -> IndexesListResponse:
        return self._make_request('GET', 'v1/resumes/list-indexes/')

    def index_resume(self, documents: List[Dict], index_name: str, id_field: str, search_fields: List[str], department_name: str|None=None) -> IndexResponse:
        extra_fields = {}
        if department_name:
            extra_fields["department_name"] = department_name
        data = {
            "documents": documents,
            "index_name": index_name,
            "id_field": id_field,
            "search_fields": search_fields,
            **extra_fields
        }
        return self._make_request('POST', 'v1/resumes/index/', json=data)

    def delete_resumes(self, documents_ids: List[str], index_name: str) -> Dict:
        data = {
            "documents_ids": documents_ids,
            "index_name": index_name
        }
        return self._make_request('POST', 'v1/resumes/delete/', json=data)

    def search_resumes(
        self, 
        query: str, 
        index_name: str, 
        filters: Optional[Dict] = None, 
        department_name: str|None=None,
        custom_query: Optional[Dict] = None,
        top_k: Optional[int] = None
    ) -> SearchResponse:
        data = {"query": query, "index_name": index_name}
        if filters:
            data["filters"] = filters
        if department_name:
            data["department_name"] = department_name
        if custom_query:
            data["custom_query"] = custom_query
        if top_k:
            data["top_k"] = top_k

        return self._make_request('POST', 'v1/resumes/search/', json=data)

    def search_jobrex_resumes(
        self, 
        query: str, 
        filters: Optional[Dict] = None,
        custom_query: Optional[Dict] = None,
        top_k: Optional[int] = None
    ) -> SearchResponse:
        data = {"query": query}
        if filters:
            data["filters"] = filters
        if custom_query:
            data["custom_query"] = custom_query
        if top_k:
            data["top_k"] = top_k
        return self._make_request('POST', 'v1/resumes/search-jobrex/', json=data)


class JobsClient(BaseClient):
    """
    Client for interacting with the Jobrex API for jobs.
    """
    # Job-related methods
    def get_candidate_score(self, job_details: Dict, resume_details: Dict,
                        threshold: float = 50.0, sections_weights: Optional[Dict] = None) -> JobMatchResult:
        data = {
            "job_details": job_details,
            "resume_details": resume_details,
            "threshold": threshold
        }
        if sections_weights:
            data["sections_weights"] = sections_weights
        return self._make_request('POST', 'v1/jobs/candidate-scoring/', json=data)

    def write_job_description(self, job_title: str, hiring_needs: str,
                             company_description: str, job_type: str,
                             job_location: str, specific_benefits: str) -> JobDetailsResponse:
        data = {
            "job_title": job_title,
            "hiring_needs": hiring_needs,
            "company_description": company_description,
            "job_type": job_type,
            "job_location": job_location,
            "specific_benefits": specific_benefits
        }
        return self._make_request('POST', 'v1/jobs/job-writing/', json=data)

    def parse_job_description(self, job_site_content: str) -> JobDetailsResponse:
        data = {
            "text": job_site_content
        }
        return self._make_request('POST', 'v1/jobs/extract-job-description/', json=data)

    def create_zoom_meeting(self, client_id: str, client_secret: str, account_id: str, duration: int, start_time: str, timezone: str, topic: str) -> ZoomMeetingResponse:
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "account_id": account_id,
            "duration": duration,
            "start_time": start_time,
            "timezone": timezone,
            "topic": topic
        }
        return self._make_request('POST', 'v1/jobs/create-zoom-meeting/', json=data)

    def list_job_indexes(self) -> IndexesListResponse:
        return self._make_request('GET', 'v1/jobs/list-indexes/')

    def search_jobs(
        self, 
        query: str, 
        index_name: str, 
        filters: Optional[Dict] = None, 
        department_name: str|None=None,
        custom_query: Optional[Dict] = None,
        top_k: Optional[int] = None
    ) -> SearchResponse:
        data = {"query": query, "index_name": index_name}
        if filters:
            data["filters"] = filters
        if department_name:
            data["department_name"] = department_name
        if custom_query:
            data["custom_query"] = custom_query
        if top_k:
            data["top_k"] = top_k
        return self._make_request('POST', 'v1/jobs/search/', json=data)

    def delete_job(self, documents_ids: List[str], index_name: str) -> Dict:
        data = {
            "documents_ids": documents_ids,
            "index_name": index_name
        }
        return self._make_request('POST', 'v1/jobs/delete/', json=data)

    def index_job(self, documents: List[Dict], index_name: str, id_field: str, search_fields: List[str], department_name: str|None=None) -> Dict:
        extra_fields = {}
        if department_name:
            extra_fields["department_name"] = department_name
        data = {
            "documents": documents,
            "index_name": index_name,
            "id_field": id_field,
            "search_fields": search_fields,
            **extra_fields

        }
        return self._make_request('POST', 'v1/jobs/index/', json=data)

    def generate_screening_questions(self, resume_details: Dict, job_details: Dict) -> Dict:
        """
        Generate screening questions based on job description and resume.

        Args:
            resume_details (Dict): Dictionary containing the candidate's resume information
            job_details (Dict): Dictionary containing the job position details

        Returns:
            Dict: Generated screening questions
        """
        data = {
            "resume_details": resume_details,
            "job_details": job_details
        }
        return self._make_request('POST', 'v1/jobs/generate-screening-questions/', json=data)

    def generate_interview_criteria(self, job_details: Dict, interview_type: str = "Technical") -> Dict:
        """
        Generate interview criteria based on job description.

        Args:
            job_details (Dict): Dictionary containing the job position details
            interview_type (str): Type of interview (technical, behavioral, etc.)

        Returns:
            Dict: Generated interview criteria
        """
        data = {
            "job_details": job_details,
            "interview_type": interview_type
        }
        return self._make_request('POST', 'v1/jobs/generate-interview-creterias/', json=data)

    def generate_offer_letter(self, job_details: Dict, user_data: Dict, salary: str = None, benefits: str = None, company_policies: str = None) -> Dict:
        """
        Generate an offer letter based on job and candidate details.

        Args:
            job_details (Dict): Dictionary containing the job position details
            user_data (Dict): Dictionary containing the candidate's information
            salary (str, optional): Salary details
            benefits (str, optional): Benefits comparison
            company_policies (str, optional): Company policies information

        Returns:
            Dict: Generated offer letter
        """
        data = {
            "job_details": job_details,
            "user_data": user_data
        }
        if salary:
            data["salary"] = salary
        if benefits:
            data["benefits"] = benefits
        if company_policies:
            data["company_policies"] = company_policies
        return self._make_request('POST', 'v1/jobs/generate-offer-letter/', json=data)

    def generate_screening_email(self, resume_details: Dict, job_details: Dict, questionnaire_responses: List[Dict]) -> Dict:
        """
        Generate a screening email based on job, resume, and questionnaire responses.

        Args:
            resume_details (Dict): Dictionary containing the candidate's resume information
            job_details (Dict): Dictionary containing the job position details
            questionnaire_responses (List[Dict]): List of questionnaire responses

        Returns:
            Dict: Generated screening email
        """
        data = {
            "resume_details": resume_details,
            "job_details": job_details,
            "questionnaire_responses": questionnaire_responses
        }
        return self._make_request('POST', 'v1/jobs/generate-screening-email/', json=data)

    def get_calendar_available_times(
        self,
        recruiter_email: str,
        date: str,
        working_start_hour: int,
        working_end_hour: int,
        time_zone: str,
        calendar_provider: str,
        calendar_credentials: Dict[str, str]
    ) -> Dict:
        """
        Get available time slots from a recruiter's calendar.

        Args:
            recruiter_email (str): Email of the recruiter whose calendar to check
            date (str): Date to check availability for in YYYY-MM-DD format
            working_start_hour (int): Start hour of working day in 24-hour format (0-23)
            working_end_hour (int): End hour of working day in 24-hour format (1-24)
            time_zone (str): Timezone for the availability check (e.g. 'America/New_York')
            calendar_provider (str): Calendar provider to use ('google' or 'outlook')
            calendar_credentials (Dict[str, str]): Dictionary containing calendar API credentials

        Returns:
            Dict: Available time slots
        """
        data = {
            "recruiter_email": recruiter_email,
            "date": date,
            "working_start_hour": working_start_hour,
            "working_end_hour": working_end_hour,
            "time_zone": time_zone,
            "calendar_provider": calendar_provider,
            "calendar_credentials": calendar_credentials
        }
        return self._make_request('POST', 'v1/jobs/get-calendar-available-times/', json=data)

    def get_zoom_transcript(self, meeting_id: str, access_token: str) -> Dict:
        """
        Retrieve transcript from a Zoom meeting.

        Args:
            meeting_id (str): ID of the Zoom meeting
            access_token (str): Zoom API access token

        Returns:
            Dict: Meeting transcript
        """
        data = {
            "meeting_id": meeting_id,
            "access_token": access_token
        }
        return self._make_request('POST', 'v1/jobs/retrieve-zoom-transcript/', json=data)

    def get_teams_transcript(self, meeting_id: str, access_token: str) -> Dict:
        """
        Retrieve transcript from a Teams meeting.

        Args:
            meeting_id (str): ID of the Teams meeting
            access_token (str): Teams API access token

        Returns:
            Dict: Meeting transcript
        """
        data = {
            "meeting_id": meeting_id,
            "access_token": access_token
        }
        return self._make_request('POST', 'v1/jobs/retrieve-teams-transcript/', json=data)

    def extract_interview_responses(
        self,
        transcript: str,
        interviewee_name: str,
        interviewer_name: str
    ) -> Dict:
        """
        Extract interview responses from a transcript.

        Args:
            transcript (str): The interview transcript in VTT format
            interviewee_name (str): Name or identifier of the interviewee
            interviewer_name (str): Name or identifier of the interviewer

        Returns:
            Dict: Extracted interview responses
        """
        data = {
            "transcript": transcript,
            "interviewee_name": interviewee_name,
            "interviewer_name": interviewer_name
        }
        return self._make_request('POST', 'v1/jobs/extract-interview-responses/', json=data)

    def generate_final_report(
        self,
        transcript: str,
        evaluation_criteria: List[Dict[str, Union[str, float]]],
        chunk_size: int = 4000,
        overlap_size: int = 200
    ) -> Dict:
        """
        Generate a final evaluation report based on an interview transcript.

        Args:
            transcript (str): The interview transcript to evaluate
            evaluation_criteria (List[Dict[str, Union[str, float]]]): List of criteria to evaluate against.
                Each criterion should have:
                - criteria_name (str): Name of the evaluation criteria
                - weight (float): Weight of this criteria in the final evaluation (0-1)
                - description (str): Description of what this criteria evaluates
            chunk_size (int, optional): Maximum size of each transcript chunk in characters. Defaults to 4000.
            overlap_size (int, optional): Size of overlap between chunks in characters. Defaults to 200.

        Returns:
            Dict: Generated evaluation report
        """
        data = {
            "transcript": transcript,
            "evaluation_criteria": evaluation_criteria,
            "chunk_size": chunk_size,
            "overlap_size": overlap_size
        }
        return self._make_request('POST', 'v1/jobs/generate-final-report/', json=data)
