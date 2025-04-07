"""
ICAI CA Scraper - A module to fetch CA member details from ICAI website.
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any, List, Optional
import re
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CAScraper:
    """A class to scrape CA member details from ICAI website"""
    
    BASE_URL = "http://112.133.194.254/lom.asp"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "http://112.133.194.254",
        "Referer": "http://112.133.194.254/lom.asp"
    }

    def __init__(self, delay_between_requests: float = 1.0):
        """Initialize the scraper
        
        Args:
            delay_between_requests: Minimum delay between requests in seconds
        """
        self.delay = delay_between_requests
        self.session = requests.Session()
        self._last_request_time = 0
    
    def _wait_for_rate_limit(self):
        """Ensure minimum delay between requests"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self._last_request_time = time.time()
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean and standardize text fields"""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'[^\w\s\-.,:#/()@]', '', text)
        return text
    
    @staticmethod
    def _extract_year(text: str) -> str:
        """Extract year from text fields"""
        if not text:
            return ""
        year_match = re.search(r'[AF]?(19|20)\d{2}', text)
        return year_match.group(0) if year_match else text.strip()
    
    @staticmethod
    def _process_name(name_text: str) -> str:
        """Process name field to remove designations"""
        if not name_text:
            return ""
        name = re.sub(r',?\s*[AF]CA\b', '', name_text)
        return CAScraper._clean_text(name)
    
    def get_member_details(self, membership_no: int) -> Optional[Dict[str, Any]]:
        """Get details for a single CA membership number
        
        Args:
            membership_no: The membership number to look up
            
        Returns:
            Dict containing member details if found, None if not found or error
        """
        self._wait_for_rate_limit()
        
        try:
            # First get the main page to get any cookies/tokens
            self.session.get(self.BASE_URL, headers=self.HEADERS, verify=False)
            
            # Submit the form
            data = {
                "t1": str(membership_no),
                "B1": "Submit"
            }
            
            response = self.session.post(
                self.BASE_URL,
                data=data,
                headers=self.HEADERS,
                timeout=15,
                verify=False
            )
            response.raise_for_status()
            
            if "no records found" in response.text.lower():
                return None
            
            soup = BeautifulSoup(response.content, "html.parser")
            tables = soup.find_all("table")
            
            member_data = {}
            current_key = None
            address_parts = []
            
            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 2:
                        key = cols[0].text.strip().replace(":", "").strip()
                        val = cols[1].text.strip()
                        
                        # Handle empty key (continuation of address)
                        if not key and current_key == "Address":
                            if val:
                                address_parts.append(val)
                            continue
                        
                        # Extract fields based on key
                        if "Name" in key:
                            member_data["name"] = self._process_name(val)
                            current_key = "Name"
                        elif "Gender" in key:
                            member_data["gender"] = self._clean_text(val)
                        elif "Address" in key:
                            address_parts = [val] if val else []
                            current_key = "Address"
                        elif "COP" in key or "Certificate of Practice" in key:
                            member_data["cop_status"] = self._clean_text(val)
                        elif "Associate" in key:
                            member_data["associate_year"] = self._extract_year(val)
                        elif "Fellow" in key:
                            member_data["fellow_year"] = self._extract_year(val)
                        elif "Qualification" in key:
                            member_data["qualification"] = self._clean_text(val)
                        elif "Date of Birth" in key:
                            member_data["date_of_birth"] = self._clean_text(val)
                        elif "Email" in key:
                            member_data["email"] = self._clean_text(val)
                        elif "Mobile" in key:
                            member_data["mobile"] = self._clean_text(val)
                        elif "Phone" in key:
                            member_data["phone"] = self._clean_text(val)
            
            # Combine address parts if any
            if address_parts:
                member_data["address"] = ", ".join(filter(None, address_parts))
            
            # Only return if we found some valid data
            if member_data and any(member_data.values()):
                member_data["membership_no"] = str(membership_no)
                member_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return member_data
            
            return None
            
        except Exception as e:
            print(f"Error fetching details for {membership_no}: {str(e)}")
            return None
    
    def get_multiple_members(self, membership_numbers: List[int]) -> Dict[str, Dict[str, Any]]:
        """Get details for multiple CA membership numbers
        
        Args:
            membership_numbers: List of membership numbers to look up
            
        Returns:
            Dict mapping membership numbers to their details
        """
        results = {}
        
        for number in membership_numbers:
            details = self.get_member_details(number)
            if details:
                results[str(number)] = details
        
        return results 