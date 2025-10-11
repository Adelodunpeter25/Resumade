import PyPDF2
import re
from io import BytesIO
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class PDFParserService:
    """Simplified but effective PDF resume parser"""
    
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
        full_text = ' '.join(lines)
        
        resume_data = {
            "personal_info": {},
            "experience": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "projects": []
        }
        
        # Extract personal info
        resume_data["personal_info"] = PDFParserService._extract_personal_info(lines, full_text)
        
        # Find sections
        sections = PDFParserService._find_sections(lines)
        
        # Extract each section
        if "experience" in sections:
            resume_data["experience"] = PDFParserService._extract_experience(sections["experience"])
        
        if "education" in sections:
            resume_data["education"] = PDFParserService._extract_education(sections["education"])
        
        if "skills" in sections:
            resume_data["skills"] = PDFParserService._extract_skills(sections["skills"])
        
        return resume_data
    
    @staticmethod
    def _extract_personal_info(lines: List[str], full_text: str) -> Dict:
        """Extract personal information"""
        personal_info = {}
        
        # Name - usually first non-empty line that's not too long
        for line in lines[:5]:
            if 2 <= len(line.split()) <= 4 and not '@' in line and not re.search(r'\d{3}', line):
                personal_info["full_name"] = line
                break
        
        # Email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', full_text)
        if email_match:
            personal_info["email"] = email_match.group()
        
        # Phone
        phone_match = re.search(r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})', full_text)
        if phone_match:
            personal_info["phone"] = phone_match.group().strip()
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', full_text, re.IGNORECASE)
        if linkedin_match:
            personal_info["linkedin"] = f"https://{linkedin_match.group()}"
        
        # Location - look for City, State pattern
        location_match = re.search(r'([A-Z][a-z]+,\s*[A-Z]{2,})', full_text)
        if location_match:
            personal_info["location"] = location_match.group()
        
        return personal_info
    
    @staticmethod
    def _find_sections(lines: List[str]) -> Dict[str, List[str]]:
        """Find major resume sections"""
        sections = {}
        current_section = None
        current_content = []
        
        section_keywords = {
            'experience': ['experience', 'work', 'employment', 'professional'],
            'education': ['education', 'academic', 'university', 'college'],
            'skills': ['skills', 'technical', 'competencies', 'technologies']
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this is a section header
            found_section = None
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords) and len(line.split()) <= 3:
                    found_section = section
                    break
            
            if found_section:
                # Save previous section
                if current_section and current_content:
                    sections[current_section] = current_content
                
                current_section = found_section
                current_content = []
            elif current_section and line.strip():
                current_content.append(line)
        
        # Save last section
        if current_section and current_content:
            sections[current_section] = current_content
        
        return sections
    
    @staticmethod
    def _extract_experience(lines: List[str]) -> List[Dict]:
        """Extract work experience"""
        experiences = []
        current_exp = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for date patterns to identify new entries
            if re.search(r'\d{4}', line) and ('-' in line or '–' in line or 'present' in line.lower()):
                if current_exp:
                    experiences.append(current_exp)
                
                current_exp = {
                    "position": "",
                    "company": "",
                    "location": "",
                    "start_date": "",
                    "end_date": "",
                    "description": "",
                    "current": False
                }
                
                # Extract dates
                date_parts = re.split(r'[-–]', line)
                if len(date_parts) >= 2:
                    current_exp["start_date"] = date_parts[0].strip()
                    end_date = date_parts[1].strip()
                    current_exp["end_date"] = end_date
                    current_exp["current"] = 'present' in end_date.lower()
            
            elif current_exp:
                # First non-date line is likely position
                if not current_exp["position"]:
                    current_exp["position"] = line
                # Second line is likely company
                elif not current_exp["company"]:
                    current_exp["company"] = line
                # Rest is description
                else:
                    if current_exp["description"]:
                        current_exp["description"] += " " + line
                    else:
                        current_exp["description"] = line
        
        if current_exp:
            experiences.append(current_exp)
        
        return experiences
    
    @staticmethod
    def _extract_education(lines: List[str]) -> List[Dict]:
        """Extract education"""
        education = []
        current_edu = None
        
        degree_keywords = ['bachelor', 'master', 'phd', 'b.s.', 'm.s.', 'b.a.', 'm.a.', 'degree']
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree keywords
            if any(keyword in line.lower() for keyword in degree_keywords):
                if current_edu:
                    education.append(current_edu)
                
                current_edu = {
                    "degree": line,
                    "institution": "",
                    "field_of_study": "",
                    "location": "",
                    "start_date": "",
                    "end_date": ""
                }
            
            elif current_edu and not current_edu["institution"]:
                current_edu["institution"] = line
            
            elif current_edu and re.search(r'\d{4}', line):
                # Extract graduation year
                year_match = re.search(r'\d{4}', line)
                if year_match:
                    current_edu["end_date"] = year_match.group()
        
        if current_edu:
            education.append(current_edu)
        
        return education
    
    @staticmethod
    def _extract_skills(lines: List[str]) -> List[Dict]:
        """Extract skills"""
        skills = []
        
        # Combine all skill lines and split by common delimiters
        skills_text = ' '.join(lines)
        skill_items = re.split(r'[,;•·\n\t]', skills_text)
        
        for item in skill_items:
            item = item.strip()
            if item and len(item) > 1 and len(item) < 50:  # Reasonable skill name length
                skills.append({
                    "name": item,
                    "level": "Intermediate"
                })
        
        return skills[:20]  # Limit to 20 skills to avoid noise
        sections = PDFParserService._identify_sections(lines)
        
        if "experience" in sections:
            resume_data["experience"] = PDFParserService._extract_experience(sections["experience"])
        
        if "education" in sections:
            resume_data["education"] = PDFParserService._extract_education(sections["education"])
        
        if "skills" in sections:
            resume_data["skills"] = PDFParserService._extract_skills(sections["skills"])
        
        return resume_data
    
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
