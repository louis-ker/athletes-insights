import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const Button = () => {
    const [isVisible, setIsVisible] = useState(true)

    const scrollToSection = () => {
    const section = document.getElementById('chatbot');
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Gestion de la visibilité du bouton
  useEffect(() => {
    const handleScroll = () => {
      const section = document.getElementById('chatbot');
      if (!section) return;

      const sectionBottom = section.offsetTop + section.offsetHeight;
      const scrollPosition = window.scrollY + window.innerHeight;

      // Si on est en dessous de la section => cacher le bouton
      if (scrollPosition >= sectionBottom) {
        setIsVisible(false);
      } else {
        setIsVisible(true);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <StyledWrapper isVisible={isVisible}>
      <button className="button" onClick={scrollToSection}>
        <svg className="svgIcon" viewBox="0 0 384 512">
          <path d="M214.6 41.4c-12.5-12.5-32.8-12.5-45.3 0l-160 160c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 141.2V448c0 17.7 14.3 32 32 32s32-14.3 32-32V141.2L329.4 246.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3l-160-160z" />
        </svg>
      </button>
    </StyledWrapper>
  );
}

const StyledWrapper = styled.div`
  .button {
    left: 50%;
    transform: translateX(-50%);
    width: 50px;
    top: 660px;
    height: 50px;
    border-radius: 50%;
    background-color: #8200cdff;
    border: 5px solid #d896ffff;
    outline: 5px solid #d896ffff;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition-duration: 0.3s;
    overflow: hidden;
    position: fixed;
    z-index: 1000;
    opacity: ${(props) => (props.isVisible ? 1 : 0)};
    pointer-events: ${(props) => (props.isVisible ? 'auto' : 'none')};
  }

  .svgIcon {
    width: 12px;
    transition-duration: 0.3s;
    transform: rotate(180deg);
  }

  .svgIcon path {
    fill: white;
  }

  .button:hover {
    width: 140px;
    border-radius: 50px;
    transition-duration: 0.3s;
    background-color: #8200cdff;
    outline: 10px solid #f2ddffff;
  }

  .button:hover .svgIcon {
    /* width: 20px; */
    transition-duration: 0.3s;
    transform: translateY(200%) rotate(180deg);
  }

  .button::before {
    position: absolute;
    bottom: -20px;
    content: "Ask Something";
    color: white;
    /* transition-duration: .3s; */
    font-size: 0px;
  }

  .button:hover::before {
    font-size: 13px;
    opacity: 1;
    bottom: unset;
    /* transform: translateY(-30px); */
    transition-duration: 0.3s;
  }`;

export default Button;
