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
      ['bold', 'italic', 'underline'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      ['clean']
    ]
  };

  const formats = [
    'bold', 'italic', 'underline',
    'list', 'bullet'
  ];

  useEffect(() => {
    // Ensure Quill is properly initialized
    if (quillRef.current) {
      const editor = quillRef.current.getEditor();
      editor.enable(true);
    }
  }, []);

  return (
    <div className="rich-text-editor">
      <ReactQuill
        ref={quillRef}
        theme="snow"
        value={value || ''}
        onChange={onChange}
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
