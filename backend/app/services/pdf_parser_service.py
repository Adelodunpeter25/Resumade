import PyPDF2
import re
from io import BytesIO
from typing import Dict, List, Tuple
from dateutil import parser as date_parser
import logging

logger = logging.getLogger(__name__)

# Common technical skills database for validation
KNOWN_SKILLS = {
    # Programming Languages
    'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust',
    'typescript', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell',
    # Web Technologies
    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi',
    'spring', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'sass', 'webpack', 'next.js', 'nuxt',
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'dynamodb',
    'elasticsearch', 'firebase', 'mariadb', 'neo4j', 'couchdb',
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'terraform',
    'ansible', 'chef', 'puppet', 'circleci', 'travis', 'heroku', 'netlify', 'vercel',
    # Data Science & ML
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
    'jupyter', 'spark', 'hadoop', 'tableau', 'power bi', 'excel', 'spss', 'sas',
    # Mobile
    'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
    # Tools & Others
    'git', 'jira', 'confluence', 'slack', 'trello', 'asana', 'figma', 'sketch', 'photoshop',
    'illustrator', 'xd', 'linux', 'unix', 'windows', 'macos', 'agile', 'scrum', 'kanban',
    'rest', 'graphql', 'soap', 'api', 'microservices', 'ci/cd', 'tdd', 'bdd',
    # Soft Skills (common ones)
    'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
    'project management', 'time management', 'analytical', 'creative'
}

# Common noise words to filter out
NOISE_WORDS = {
    'and', 'or', 'with', 'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'by',
    'from', 'as', 'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must',
    'can', 'etc', 'including', 'such', 'like', 'using', 'used'
}

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
    def _parse_date_range(text: str) -> Tuple[str, str, bool]:
        """Parse date range from text like 'Jan 2020 - Present' or '2020-2022'"""
        text = text.strip()
        text_lower = text.lower()
        is_current = 'present' in text_lower or 'current' in text_lower or 'now' in text_lower
        
        # Split by common separators
        parts = re.split(r'\s*[-–—to]\s*', text, maxsplit=1, flags=re.IGNORECASE)
        
        start_date = ""
        end_date = ""
        
        # Parse start date
        if len(parts) > 0:
            try:
                parsed = date_parser.parse(parts[0], fuzzy=True)
                start_date = parsed.strftime("%Y-%m")
            except:
                # Fallback to year extraction
                year_match = re.search(r'\b(19|20)\d{2}\b', parts[0])
                if year_match:
                    start_date = year_match.group()
        
        # Parse end date
        if len(parts) > 1:
            if is_current:
                end_date = "Present"
            else:
                try:
                    parsed = date_parser.parse(parts[1], fuzzy=True)
                    end_date = parsed.strftime("%Y-%m")
                except:
                    # Fallback to year extraction
                    year_match = re.search(r'\b(19|20)\d{2}\b', parts[1])
                    if year_match:
                        end_date = year_match.group()
        elif is_current:
            end_date = "Present"
        
        return start_date, end_date, is_current
    
    @staticmethod
    def _is_valid_skill(skill: str) -> bool:
        """Validate if a string is a legitimate skill"""
        skill_lower = skill.lower().strip()
        
        # Filter out noise words
        if skill_lower in NOISE_WORDS:
            return False
        
        # Filter out very short or very long strings
        if len(skill) < 2 or len(skill) > 50:
            return False
        
        # Filter out strings with too many special characters
        special_char_count = sum(1 for c in skill if not c.isalnum() and c not in [' ', '.', '+', '#', '-', '/'])
        if special_char_count > 2:
            return False
        
        # Check if it's a known skill (case-insensitive)
        if skill_lower in KNOWN_SKILLS:
            return True
        
        # Check for partial matches (e.g., "Node.js" matches "node.js")
        for known_skill in KNOWN_SKILLS:
            if known_skill in skill_lower or skill_lower in known_skill:
                return True
        
        # If it looks like a technology (contains version numbers, dots, etc.)
        if re.search(r'\d+\.?\d*', skill) or '.' in skill or '+' in skill or '#' in skill:
            return True
        
        # If it's capitalized and reasonable length (likely a proper noun/technology)
        if skill[0].isupper() and 3 <= len(skill) <= 30:
            return True
        
        return False
    
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
        
        if "projects" in sections:
            resume_data["projects"] = PDFParserService._extract_projects(sections["projects"])
        
        if "certifications" in sections:
            resume_data["certifications"] = PDFParserService._extract_certifications(sections["certifications"])
        
        return resume_data
    
    @staticmethod
    def _extract_personal_info(lines: List[str], full_text: str) -> Dict:
        """Extract personal information"""
        personal_info = {}
        
        # Name - usually first non-empty line that's not too long
        for line in lines[:5]:
            if 2 <= len(line.split()) <= 4 and '@' not in line and not re.search(r'\d{3}', line):
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
            'skills': ['skills', 'technical', 'competencies', 'technologies'],
            'projects': ['projects', 'portfolio', 'personal projects'],
            'certifications': ['certifications', 'certificates', 'licenses', 'credentials']
        }
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this is a section header
            found_section = None
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords) and len(line.split()) <= 4:
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
            has_date = re.search(r'\b(19|20)\d{2}\b', line)
            has_separator = any(sep in line for sep in ['-', '–', '—', 'to', 'present', 'current'])
            
            if has_date and has_separator:
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
                
                # Parse dates using improved parser
                start_date, end_date, is_current = PDFParserService._parse_date_range(line)
                current_exp["start_date"] = start_date
                current_exp["end_date"] = end_date
                current_exp["current"] = is_current
            
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
            
            elif current_edu and re.search(r'\b(19|20)\d{2}\b', line):
                # Parse date range if present
                if any(sep in line for sep in ['-', '–', 'to']):
                    start_date, end_date, _ = PDFParserService._parse_date_range(line)
                    current_edu["start_date"] = start_date
                    current_edu["end_date"] = end_date
                else:
                    # Single year (graduation year)
                    try:
                        parsed = date_parser.parse(line, fuzzy=True)
                        current_edu["end_date"] = parsed.strftime("%Y")
                    except:
                        year_match = re.search(r'\b(19|20)\d{2}\b', line)
                        if year_match:
                            current_edu["end_date"] = year_match.group()
        
        if current_edu:
            education.append(current_edu)
        
        return education
    
    @staticmethod
    def _extract_skills(lines: List[str]) -> List[Dict]:
        """Extract skills with validation"""
        skills = []
        seen_skills = set()  # Track duplicates
        
        # Combine all skill lines and split by common delimiters
        skills_text = ' '.join(lines)
        skill_items = re.split(r'[,;•·\n\t|]', skills_text)
        
        for item in skill_items:
            item = item.strip()
            
            # Skip empty or invalid items
            if not item:
                continue
            
            # Validate skill
            if PDFParserService._is_valid_skill(item):
                # Normalize for duplicate detection
                item_lower = item.lower()
                if item_lower not in seen_skills:
                    seen_skills.add(item_lower)
                    skills.append({
                        "name": item,
                        "level": "Intermediate"
                    })
        
        return skills[:25]  # Limit to 25 skills
    
    @staticmethod
    def _extract_projects(lines: List[str]) -> List[Dict]:
        """Extract projects"""
        projects = []
        current_project = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for date patterns or project indicators
            if re.search(r'\d{4}', line) or (not current_project and len(line.split()) <= 8):
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    "name": line,
                    "description": "",
                    "technologies": "",
                    "url": ""
                }
            
            elif current_project:
                # Look for URLs
                url_match = re.search(r'https?://[^\s]+', line)
                if url_match:
                    current_project["url"] = url_match.group()
                # Add to description
                else:
                    if current_project["description"]:
                        current_project["description"] += " " + line
                    else:
                        current_project["description"] = line
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    @staticmethod
    def _extract_certifications(lines: List[str]) -> List[Dict]:
        """Extract certifications"""
        certifications = []
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            # Extract date if present
            date = ""
            if re.search(r'\b(19|20)\d{2}\b', line):
                try:
                    parsed = date_parser.parse(line, fuzzy=True)
                    date = parsed.strftime("%Y-%m")
                except:
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    if year_match:
                        date = year_match.group()
            
            # Remove date from name
            name = re.sub(r'\b(19|20)\d{2}\b', '', line).strip()
            name = re.sub(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b', '', name, flags=re.IGNORECASE).strip()
            
            # Extract issuer (usually after " - " or " by ")
            issuer = ""
            if " - " in name:
                parts = name.split(" - ", 1)
                name = parts[0].strip()
                issuer = parts[1].strip()
            elif " by " in name.lower():
                parts = re.split(r'\s+by\s+', name, flags=re.IGNORECASE)
                name = parts[0].strip()
                issuer = parts[1].strip() if len(parts) > 1 else ""
            
            certifications.append({
                "name": name,
                "issuer": issuer,
                "date": date
            })
        
        return certifications

