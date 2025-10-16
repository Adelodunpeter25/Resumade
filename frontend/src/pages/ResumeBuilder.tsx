import { useState, createElement } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, Save, Palette, BarChart3, History, Check, LogIn, Download, ChevronDown, Upload } from 'lucide-react';
import type { Resume } from '../types';
import { useErrorHandler, useResumeBuilder, usePreview, useResumeActions } from '../hooks';
import ErrorNotification from '../components/common/ErrorNotification';
import ErrorBoundary from '../components/common/ErrorBoundary';
import { API_BASE_URL } from '../services/api';

import PersonalInfoForm from '../components/resume/PersonalInfoForm';
import ExperienceForm from '../components/resume/ExperienceForm';
import EducationForm from '../components/resume/EducationForm';
import SkillsForm from '../components/resume/SkillsForm';
import CertificationsForm from '../components/resume/CertificationsForm';
import ProjectsForm from '../components/resume/ProjectsForm';
import TemplateCustomizer from '../components/resume/TemplateCustomizer';
import PDFUploader from '../components/resume/PDFUploader';
import SectionManager from '../components/resume/SectionManager';
import CustomSectionForm from '../components/resume/CustomSectionForm';

export default function ResumeBuilder() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { error, hideError } = useErrorHandler();
  
  // Local UI state
  const [currentStep, setCurrentStep] = useState(0);
  const [showTemplateDropdown, setShowTemplateDropdown] = useState(false);
  const [showExportDropdown, setShowExportDropdown] = useState(false);
  const [showPDFUploader, setShowPDFUploader] = useState(false);
  const [hoveredTemplate, setHoveredTemplate] = useState<string | null>(null);
  
  // Custom hooks for organized logic
  const {
    resume, templates, saving, saveStatus, loading, isAuthenticated,
    handleSave, updateResumeData
  } = useResumeBuilder(id);
  
  const { previewIframeRef } = usePreview(resume, hoveredTemplate);
  const { downloading, handleDownload, handleFeatureClick } = useResumeActions(resume, isAuthenticated, id);

  // Generate dynamic steps including custom sections
  const allSteps = [
    { id: 'personal', label: 'Personal Info', component: PersonalInfoForm },
    { id: 'experience', label: 'Experience', component: ExperienceForm },
    { id: 'education', label: 'Education', component: EducationForm },
    { id: 'skills', label: 'Skills', component: SkillsForm },
    { id: 'certifications', label: 'Certifications', component: CertificationsForm },
    { id: 'projects', label: 'Projects', component: ProjectsForm },
    ...(resume.custom_sections || []).map((section: any) => ({
      id: section.id,
      label: section.title || section.name,
      component: CustomSectionForm,
      isCustom: true
    })),
    { id: 'sections', label: 'Manage Sections', component: SectionManager }
  ];

  // UI helper functions
  const handlePDFDataExtracted = (extractedData: Partial<Resume>) => {
    updateResumeData('personal_info', { ...resume.personal_info, ...extractedData.personal_info });
    updateResumeData('experience', extractedData.experience || []);
    updateResumeData('education', extractedData.education || []);
    updateResumeData('skills', extractedData.skills || []);
  };

  const changeTemplate = (templateName: string) => {
    updateResumeData('template_name', templateName);
  };

  const handleLoginPrompt = () => {
    // Save resume data to localStorage before redirecting
    localStorage.setItem('guest_resume', JSON.stringify(resume));
    localStorage.setItem('redirect_after_login', `/resume/${id || 'new'}`);
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const currentStepData = allSteps[currentStep];
  const CurrentStepComponent = currentStepData.component;
  
  // For custom sections, pass specific props
  const customSectionProps = 'isCustom' in currentStepData && currentStepData.isCustom ? {
    sectionName: currentStepData.label,
    items: resume.custom_sections?.find((s: any) => s.id === currentStepData.id)?.items || [],
    onChange: (items: any) => {
      const updatedSections = (resume.custom_sections || []).map((s: any) =>
        s.id === currentStepData.id ? { ...s, items } : s
      );
      updateResumeData('custom_sections', updatedSections);
    }
  } : {};

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        <ErrorNotification
          message={error.message}
          type={error.type}
          visible={error.visible}
          onClose={hideError}
        />
        {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate(-1)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <ArrowLeft size={20} />
              </button>
              <input
                type="text"
                value={resume.title}
                onChange={(e) => updateResumeData('title', e.target.value)}
                className="text-xl font-bold border-none focus:outline-none focus:ring-2 focus:ring-emerald-500 rounded px-2"
              />
              <span className="text-sm text-gray-500">
                {saveStatus === 'saving' && '💾 Saving...'}
                {saveStatus === 'saved' && <span className="flex items-center gap-1 text-green-600"><Check size={16} /> Saved</span>}
                {saveStatus === 'unsaved' && '⚠️ Unsaved changes'}
              </span>
              {!isAuthenticated && (
                <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                  Guest Mode
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <div className="relative">
                <button
                  onClick={() => setShowTemplateDropdown(!showTemplateDropdown)}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  <Palette size={20} />
                  <span>Templates</span>
                </button>
              </div>
              <button
                onClick={() => setShowPDFUploader(true)}
                className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                title="Import from LinkedIn PDF or existing resume"
              >
                <Upload size={20} />
                <span>Import PDF</span>
              </button>
              {isAuthenticated && (
                <>
                  <button
                    onClick={() => handleFeatureClick('versions')}
                    className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                    title="Version History"
                  >
                    <History size={20} />
                  </button>
                  <button
                    onClick={() => handleFeatureClick('ats')}
                    className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                    title="ATS Score"
                  >
                    <BarChart3 size={20} />
                    <span className="hidden sm:inline">ATS Score</span>
                  </button>
                </>
              )}
              <div className="relative">
                <button
                  onClick={() => setShowExportDropdown(!showExportDropdown)}
                  disabled={downloading}
                  className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                  title="Export Resume"
                >
                  <Download size={20} />
                  <span>Export</span>
                  <ChevronDown size={16} />
                </button>
                {showExportDropdown && (
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 z-20">
                    <button
                      onClick={() => {
                        handleDownload('pdf');
                        setShowExportDropdown(false);
                      }}
                      className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100"
                    >
                      <div className="font-medium text-gray-900">PDF</div>
                      <div className="text-xs text-gray-500">Portable Document Format</div>
                    </button>
                    {isAuthenticated && (
                      <>
                        <button
                          onClick={() => {
                            handleDownload('docx');
                            setShowExportDropdown(false);
                          }}
                          className="w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100"
                        >
                          <div className="font-medium text-gray-900">DOCX</div>
                          <div className="text-xs text-gray-500">Microsoft Word Document</div>
                        </button>
                        <button
                          onClick={() => {
                            handleDownload('txt');
                            setShowExportDropdown(false);
                          }}
                          className="w-full text-left px-4 py-3 hover:bg-gray-50"
                        >
                          <div className="font-medium text-gray-900">TXT</div>
                          <div className="text-xs text-gray-500">Plain Text Format</div>
                        </button>
                      </>
                    )}
                  </div>
                )}
              </div>
              {!isAuthenticated && (
                <button
                  onClick={handleLoginPrompt}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  <LogIn size={20} />
                  <span>Login to Save</span>
                </button>
              )}
              {isAuthenticated && (
                <button
                  onClick={() => handleSave(false)}
                  disabled={saving}
                  className="flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-600 text-white px-4 py-2 rounded-lg hover:from-emerald-700 hover:to-teal-700 disabled:opacity-50"
                >
                  <Save size={20} />
                  <span>{saving ? 'Saving...' : 'Save'}</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-12 gap-6">
          {/* Steps Sidebar / Template Selector */}
          <div className={showTemplateDropdown ? "col-span-3" : "col-span-2"}>
            {showTemplateDropdown ? (
              <div className="bg-white rounded-lg shadow p-4 sticky top-24">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="font-semibold text-gray-900">Templates</h3>
                  <button
                    onClick={() => setShowTemplateDropdown(false)}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    ✕
                  </button>
                </div>
                <div className="space-y-3 max-h-[calc(100vh-200px)] overflow-y-auto">
                  {templates.all_templates?.map((template) => (
                    <button
                      key={template.name}
                      onClick={() => changeTemplate(template.name)}
                      onMouseEnter={() => setHoveredTemplate(template.name)}
                      onMouseLeave={() => setHoveredTemplate(null)}
                      className={`w-full text-left p-3 rounded-lg border-2 transition-all ${
                        resume.template_name === template.name
                          ? 'border-emerald-500 bg-emerald-50'
                          : 'border-gray-200 hover:border-emerald-300'
                      }`}
                    >
                      <div className="aspect-[8.5/11] bg-gray-50 rounded mb-2 overflow-hidden border relative">
                        <iframe
                          src={`${API_BASE_URL}/api/resumes/templates/preview?template=${template.name}`}
                          className="w-full h-full border-0 pointer-events-none scale-[0.25] origin-top-left"
                          style={{ width: '400%', height: '400%' }}
                          title={`${template.display_name} Preview`}
                        />
                      </div>
                      <div className="font-medium text-sm">{template.display_name}</div>
                      <div className="text-xs text-gray-500 mt-1">{template.description}</div>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow p-4 sticky top-24">
                <h3 className="font-semibold text-gray-900 mb-4">Sections</h3>
                <nav className="space-y-2">
                  {allSteps.map((step, index) => (
                    <button
                      key={step.id}
                      onClick={() => setCurrentStep(index)}
                      className={`w-full text-left px-4 py-2 rounded-lg transition-colors text-sm ${
                        currentStep === index
                          ? 'bg-emerald-50 text-emerald-600 font-medium'
                          : 'text-gray-600 hover:bg-gray-50'
                      }`}
                    >
                      {step.label}
                    </button>
                  ))}
                </nav>
              </div>
            )}
          </div>

          {/* Form Content */}
          <div className={showTemplateDropdown ? "col-span-4" : "col-span-5"}>
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                {allSteps[currentStep].label}
              </h2>
              {'isCustom' in currentStepData && currentStepData.isCustom ? (
                <CustomSectionForm
                  sectionName={customSectionProps.sectionName}
                  items={customSectionProps.items}
                  onChange={customSectionProps.onChange}
                />
              ) : currentStepData.component === SectionManager ? (
                <SectionManager
                  resume={resume}
                  onChange={updateResumeData}
                />
              ) : (
                createElement(CurrentStepComponent as any, {
                  data: resume,
                  onChange: updateResumeData,
                  resume: resume
                })
              )}
              
              {/* Navigation Buttons */}
              <div className="flex justify-between mt-8 pt-6 border-t border-gray-200">
                <button
                  onClick={() => setCurrentStep(prev => Math.max(0, prev - 1))}
                  disabled={currentStep === 0}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
                >
                  Previous
                </button>
                {currentStep === allSteps.length - 1 ? (
                  isAuthenticated && (
                    <button
                      onClick={() => navigate(`/resume/${id}/preview`)}
                      className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                    >
                      View Resume
                    </button>
                  )
                ) : (
                  <button
                    onClick={() => setCurrentStep(prev => Math.min(allSteps.length - 1, prev + 1))}
                    className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                  >
                    Next
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Live Preview */}
          <div className="col-span-5">
            <div className="bg-white rounded-lg shadow sticky top-24">
              <div className="p-4 border-b border-gray-200">
                <h3 className="font-semibold text-gray-900">Live Preview</h3>
              </div>
              <iframe
                ref={previewIframeRef}
                name="preview-frame"
                className="w-full border-0"
                style={{ height: 'calc(100vh - 180px)' }}
                title="Resume Preview"
              />
            </div>
          </div>
        </div>
      </div>
      
      {showPDFUploader && (
        <PDFUploader
          onDataExtracted={handlePDFDataExtracted}
          onClose={() => setShowPDFUploader(false)}
        />
      )}
      </div>
    </ErrorBoundary>
  );
}
