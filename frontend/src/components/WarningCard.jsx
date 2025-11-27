import React from 'react';
import styled from 'styled-components';

const WarningCard = ({ visible, onConfirm, onCancel }) => {
  if (!visible) return null;

  return (
    <StyledWrapper>
      <div className="card">
        <div className="header">
          <div className="image">
            <svg aria-hidden="true" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24" fill="none">
              <path d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12z" 
                strokeLinejoin="round" strokeLinecap="round" />
            </svg>
          </div>
          <div className="content">
            <span className="title">Replace Widget?</span>
            <p className="message">
              This zone already contains a chart.
            </p>
          </div>
          <div className="actions">
            <button className="desactivate" type="button" onClick={onConfirm}>
              Yes, replace
            </button>
            <button className="cancel" type="button" onClick={onCancel}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  position: fixed;             /* toujours visible */
  top: 0;
  left: 0;
  width: 100vw;                /* prend tout l'écran */
  height: 100vh;
  display: flex;               /* centre le contenu */
  justify-content: center;
  align-items: center;
  background: rgba(0,0,0,0.35); /* overlay gris transparent */
  z-index: 9999;               /* passe devant tout */

  .card {
    overflow: hidden;
    position: relative;
    background-color: #ffffff;
    text-align: left;
    border-radius: 0.5rem;
    max-width: 290px;
    box-shadow:
      0 20px 25px -5px rgba(0, 0, 0, 0.1),
      0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  .header {
    padding: 1.25rem 1rem 1rem 1rem;
    background-color: #ffffff;
  }

  .image {
    display: flex;
    margin-left: auto;
    margin-right: auto;
    background-color: #fee2e2;
    flex-shrink: 0;
    justify-content: center;
    align-items: center;
    width: 3rem;
    height: 3rem;
    border-radius: 9999px;
  }

  .image svg {
    color: #dc2626;
    width: 1.5rem;
    height: 1.5rem;
  }

  .content {
    margin-top: 0.75rem;
    text-align: center;
  }

  .title {
    color: #111827;
    font-size: 1rem;
    font-weight: 600;
    line-height: 1.5rem;
  }

  .message {
    margin-top: 0.5rem;
    color: #6b7280;
    font-size: 0.875rem;
    line-height: 1.25rem;
  }

  .actions {
    margin: 0.75rem 1rem;
    background-color: #f9fafb;
  }

  .desactivate {
    display: inline-flex;
    padding: 0.5rem 1rem;
    background-color: #dc2626;
    color: #ffffff;
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 500;
    justify-content: center;
    width: 100%;
    border-radius: 0.375rem;
    border-width: 1px;
    border-color: transparent;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  }

  .cancel {
    display: inline-flex;
    margin-top: 0.75rem;
    padding: 0.5rem 1rem;
    background-color: #ffffff;
    color: #374151;
    font-size: 1rem;
    line-height: 1.5rem;
    font-weight: 500;
    justify-content: center;
    width: 100%;
    border-radius: 0.375rem;
    border: 1px solid #d1d5db;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  }

  button {
    cursor: pointer;
  }`;

export default WarningCard;
