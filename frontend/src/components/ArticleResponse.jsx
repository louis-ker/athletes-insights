import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ArticleResponse.css";

export default function ArticleResponse({ data }) {
  if (!data) return null;

  const { header, part1, part2, part3, _originalQuestion } = data;
  const sections = [part1, part2, part3].filter(Boolean);

  return (
    <article className="ai-article">
      <header className="ai-article-header">
        {_originalQuestion && (
          <p className="ai-article-question">
            Your question : <span>{_originalQuestion}</span>
          </p>
        )}

        {header?.content && (
          <h1 className="ai-article-title">
            {header.content}
          </h1>
        )}
      </header>

      <div className="ai-article-meta">
        <span className="chip chip-primary">AI-guided response</span>
        <span className="chip">Short track · Speed skating</span>
      </div>

      {sections.map((section, idx) => (
        <section key={idx} className="ai-article-section">
          {section.title && (
            <h2 className="ai-article-section-title">
              {section.title}
            </h2>
          )}

          {/* ✅ wrapper pour la classe, plus de className sur ReactMarkdown */}
          <div className="ai-article-body">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {section.generated_answer || section.content}
            </ReactMarkdown>
          </div>
        </section>
      ))}
    </article>
  );
}
