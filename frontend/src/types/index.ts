export interface User {
  id: number;
  email: string;
  full_name: string;
  created_at: string;
  is_active: boolean;
}

export interface Resume {
  id: number;
  user_id: number;
  title: string;
  template_name: string;
  template?: string;
  personal_info: PersonalInfo;
  experience: Experience[];
  education: Education[];
  skills: Skill[];
  certifications: Certification[];
  projects: Project[];
  customization?: TemplateCustomization;
  section_names?: Record<string, string>;
  custom_sections?: CustomSection[];
  ats_score?: number;
  created_at: string;
  updated_at: string;
}

export interface CustomSection {
  id: string;
  name: string;
  data: any[];
}

export interface TemplateCustomization {
  primary_color: string;
  secondary_color: string;
  font_family: string;
  font_size: string;
  line_height: string;
  margin: string;
}

export interface PersonalInfo {
  full_name: string;
  email: string;
  phone: string;
  location: string;
  linkedin?: string;
  website?: string;
  summary?: string;
}

export interface Experience {
  company: string;
  position: string;
  location: string;
  start_date: string;
  end_date?: string;
  current: boolean;
  description: string;
}

export interface Education {
  institution: string;
  degree: string;
  field_of_study: string;
  location: string;
  start_date: string;
  end_date?: string;
  gpa?: string;
}

export interface Skill {
  name: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
}

export interface Certification {
  name: string;
  issuer: string;
  date: string;
  credential_id?: string;
}

export interface Project {
  name: string;
  description: string;
  technologies: string[];
  url?: string;
}

export interface ShareLink {
  id: number;
  resume_id: number;
  token: string;
  slug?: string;
  expires_at: string;
  is_active: boolean;
  created_at: string;
}

export interface ResumeVersion {
  id: number;
  resume_id: number;
  version_number: number;
  title?: string;
  template?: string;
  personal_info?: PersonalInfo;
  experience?: Experience[];
  education?: Education[];
  skills?: Skill[];
  certifications?: Certification[];
  projects?: Project[];
  content?: Resume;
  created_at: string;
}

export interface Template {
  name: string;
  display_name: string;
  description: string;
  category: string;
  industry: string[];
  ats_score: number;
  preview_url?: string;
}

export interface APIResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}
