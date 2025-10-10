import { useEffect, useRef } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

interface RichTextEditorProps {
  value: string;
  onChange: (content: string) => void;
  placeholder?: string;
}

export default function RichTextEditor({ value, onChange, placeholder }: RichTextEditorProps) {
  const quillRef = useRef<ReactQuill>(null);

  const modules = {
    toolbar: [
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'indent': '-1'}, { 'indent': '+1' }],
      ['link'],
      ['clean']
    ]
  };

  const formats = [
    'bold', 'italic', 'underline', 'strike',
    'list', 'bullet', 'indent',
    'link'
  ];

  useEffect(() => {
    return () => {
      // Clear any active selections on unmount
      if (quillRef.current) {
        try {
          const editor = quillRef.current.getEditor();
          editor.blur();
        } catch (e) {
          // Ignore errors during cleanup
        }
      }
    };
  }, []);

  const handleChange = (content: string) => {
    // Prevent onChange from firing during unmount
    if (quillRef.current) {
      onChange(content);
    }
  };

  return (
    <div className="rich-text-editor">
      <ReactQuill
        ref={quillRef}
        theme="snow"
        value={value || ''}
        onChange={handleChange}
        modules={modules}
        formats={formats}
        placeholder={placeholder}
        className="h-[200px] mb-12"
      />
      <style jsx global>{`
        .rich-text-editor .ql-container {
          font-size: 14px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        .rich-text-editor .ql-editor {
          min-height: 150px;
          max-height: 400px;
          overflow-y: auto;
        }
      `}</style>
    </div>
  );
}
