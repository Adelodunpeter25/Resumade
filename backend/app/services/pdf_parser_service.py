import PyPDF2
import re
from io import BytesIO
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PDFParserService:
    """Service for parsing resume data from PDF files"""
    
    @staticmethod
    def parse_resume_pdf(pdf_content: bytes) -> Dict:
        """Extract resume data from PDF content"""
        try:
            # Extract text from PDF
            text = PDFParserService._extract_text_from_pdf(pdf_content)
            
            # Parse the extracted text
            resume_data = PDFParserService._parse_resume_text(text)
            
            return resume_data
            
        except Exception as e:
            logger.error(f"PDF parsing failed: {str(e)}")
            raise Exception(f"Failed to parse PDF: {str(e)}")
    
    @staticmethod
    def _extract_text_from_pdf(pdf_content: bytes) -> str:
        """Extract text content from PDF bytes"""
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        return text
    
    @staticmethod
    def _parse_resume_text(text: str) -> Dict:
        """Parse resume text and extract structured data"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        resume_data = {
            "personal_info": {},
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "projects": []
        }
        
        # Extract personal info
        resume_data["personal_info"] = PDFParserService._extract_personal_info(lines)
        
        # Extract sections
        sections = PDFParserService._identify_sections(lines)
        
        if "experience" in sections:
            resume_data["experience"] = PDFParserService._extract_experience(sections["experience"])
        
        if "education" in sections:
            resume_data["education"] = PDFParserService._extract_education(sections["education"])
        
        if "skills" in sections:
            resume_data["skills"] = PDFParserService._extract_skills(sections["skills"])
        
        return resume_data
    
    @staticmethod
    def _extract_personal_info(lines: List[str]) -> Dict:
        """Extract personal information from the first few lines"""
        personal_info = {}
        
        # Usually name is in the first few lines
        for i, line in enumerate(lines[:5]):
            if len(line.split()) <= 4 and len(line) > 5:  # Likely a name
                personal_info["full_name"] = line
                break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        for line in lines[:15]:
            email_match = re.search(email_pattern, line)
            if email_match:
                personal_info["email"] = email_match.group()
                break
        
        # Extract phone
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        for line in lines[:15]:
            phone_match = re.search(phone_pattern, line)
            if phone_match:
                personal_info["phone"] = phone_match.group()
                break
        
        # Extract LinkedIn (common in LinkedIn PDFs)
        linkedin_patterns = [
            r'linkedin\.com/in/[\w-]+',
            r'www\.linkedin\.com/in/[\w-]+',
            r'/in/[\w-]+'
        ]
        for line in lines[:20]:
            for pattern in linkedin_patterns:
                linkedin_match = re.search(pattern, line.lower())
                if linkedin_match:
                    url = linkedin_match.group()
                    if not url.startswith('http'):
                        url = f"https://linkedin.com{url}" if url.startswith('/') else f"https://{url}"
                    personal_info["linkedin"] = url
                    break
            if "linkedin" in personal_info:
                break
        
        # Extract location (often appears after name in LinkedIn PDFs)
        location_keywords = ['location', 'based in', 'from']
        for i, line in enumerate(lines[:10]):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in location_keywords):
                # Location might be on this line or the next
                if i + 1 < len(lines):
                    potential_location = lines[i + 1].strip()
                    if len(potential_location.split()) <= 4 and ',' in potential_location:
                        personal_info["location"] = potential_location
                        break
        
        # Extract summary/headline (LinkedIn PDFs often have a headline)
        summary_keywords = ['summary', 'about', 'headline', 'professional summary']
        for i, line in enumerate(lines[:20]):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in summary_keywords):
                # Summary content is usually in the next few lines
                summary_lines = []
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j] and not lines[j].isupper() and len(lines[j]) > 20:
                        summary_lines.append(lines[j])
                    elif summary_lines:  # Stop if we hit a section break
                        break
                if summary_lines:
                    personal_info["summary"] = ' '.join(summary_lines)
                    break
        
        return personal_info
    
    @staticmethod
    def _identify_sections(lines: List[str]) -> Dict[str, List[str]]:
        """Identify different sections in the resume"""
        sections = {}
        current_section = None
        section_content = []
        
        section_keywords = {
            "experience": ["experience", "work experience", "employment", "work history"],
            "education": ["education", "academic background", "qualifications"],
            "skills": ["skills", "technical skills", "competencies", "expertise"],
            "projects": ["projects", "portfolio"],
            "certifications": ["certifications", "certificates", "licenses"]
        }
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if this line is a section header
            section_found = None
            for section_name, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    section_found = section_name
                    break
            
            if section_found:
                # Save previous section
                if current_section and section_content:
                    sections[current_section] = section_content
                
                # Start new section
                current_section = section_found
                section_content = []
            elif current_section:
                section_content.append(line)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = section_content
        
        return sections
    
    @staticmethod
    def _extract_experience(lines: List[str]) -> List[Dict]:
        """Extract work experience from lines"""
        experiences = []
        current_exp = {}
        
        for line in lines:
            # Look for job titles and companies (usually contain |, -, or at)
            if any(sep in line for sep in ['|', ' - ', ' at ']):
                if current_exp:
                    experiences.append(current_exp)
                
                parts = re.split(r'\s*[\|\-]\s*|\s+at\s+', line)
                current_exp = {
                    "position": parts[0].strip() if len(parts) > 0 else "",
                    "company": parts[1].strip() if len(parts) > 1 else "",
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "current": False,
                    "description": ""
                }
            
            # Look for dates
            elif re.search(r'\d{4}', line) and current_exp:
                date_match = re.findall(r'\b\d{4}\b', line)
                if len(date_match) >= 2:
                    current_exp["start_date"] = date_match[0]
                    current_exp["end_date"] = date_match[1]
                elif len(date_match) == 1:
                    if "present" in line.lower():
                        current_exp["start_date"] = date_match[0]
                        current_exp["current"] = True
            
            # Add to description if we have a current experience
            elif current_exp and line and not line.isupper():
                if current_exp["description"]:
                    current_exp["description"] += "\n" + line
                else:
                    current_exp["description"] = line
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    @staticmethod
    def _extract_education(lines: List[str]) -> List[Dict]:
        """Extract education from lines"""
        education = []
        current_edu = {}
        
        for line in lines:
            # Look for degree patterns
            degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'diploma', 'certificate']
            if any(keyword in line.lower() for keyword in degree_keywords):
                if current_edu:
                    education.append(current_edu)
                
                current_edu = {
                    "degree": line,
                    "field_of_study": "",
                    "institution": "",
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "gpa": ""
                }
            
            # Look for institution names (usually proper nouns)
            elif current_edu and line and line[0].isupper() and not re.search(r'\d{4}', line):
                if not current_edu["institution"]:
                    current_edu["institution"] = line
            
            # Look for dates
            elif current_edu and re.search(r'\d{4}', line):
                date_match = re.findall(r'\b\d{4}\b', line)
                if len(date_match) >= 2:
                    current_edu["start_date"] = date_match[0]
                    current_edu["end_date"] = date_match[1]
        
        if current_edu:
            education.append(current_edu)
        
        return education
    
    @staticmethod
    def _extract_skills(lines: List[str]) -> List[Dict]:
        """Extract skills from lines"""
        skills = []
        
        for line in lines:
            # Split by common separators
            skill_items = re.split(r'[,;•·\n]', line)
            
            for item in skill_items:
                item = item.strip()
                if item and len(item) > 1:
                    skills.append({
                        "name": item,
                        "level": ""
                    })
        
        return skills[:20]  # Limit to 20 skills
