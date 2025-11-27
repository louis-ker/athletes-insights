import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';

const DEFAULT_STEPS = [
  { label: "Loading ISU data (1/5)", durationMs: 11_000 },
  { label: "Retrieving useful chunks (2/5)", durationMs: 10_000 },
  { label: "Generating article canva (3/5)", durationMs: 12_000 },
  { label: "Assessing graph need (4/5)", durationMs: 15_000 },
  { label: "Finalizing answer (5/5)", durationMs: 10_000 },
];

const Loader = ({ steps = DEFAULT_STEPS }) => {
  const [idx, setIdx] = useState(0);
  const timersRef = useRef([]);

  useEffect(() => {
    // reset à chaque (ré)montage
    setIdx(0);
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];

    // programme la progression des messages
    let elapsed = 0;
    for (let i = 1; i < steps.length; i++) {
      elapsed += steps[i - 1].durationMs;
      const t = setTimeout(() => setIdx(i), elapsed);
      timersRef.current.push(t);
    }

    return () => {
      timersRef.current.forEach(clearTimeout);
      timersRef.current = [];
    };
  }, [steps]);

  return (
    <StyledWrapper aria-live="polite">
      <div className="spinner">
        <div className="inner"></div>
      </div>
      <p className="message">{steps[idx]?.label}</p>
    </StyledWrapper>
  );
};

// const StyledWrapper = styled.div`
//   display: grid;
//   place-items: center;
//   gap: 12px;

//   .spinner {
//     width: 40px;
//     height: 40px;
//     border-radius: 100%;
//     background-color: aqua;
//     display: grid;
//     place-items: center;
//     animation: zoomin 1.5s infinite alternate-reverse;
//     position: relative;
//   }

//   .inner {
//     background-color: #000000ff;
//     width: 80%;
//     height: 80%;
//     border-radius: 100%;
//   }

//   .message {
//     font-size: 0.95rem;
//     opacity: 0.9;
//     margin: 0;
//     text-align: center;
//   }

//   @keyframes zoomin {
//     0% {
//       transform: scale(1);
//       box-shadow: 0 0 100px 20px rgb(16, 71, 71);
//     }
//     100% {
//       transform: scale(1.5);
//       box-shadow: 0 0 100px 20px #000;
//     }
//   }
// `;

const StyledWrapper = styled.div`
  display: grid;
  place-items: center;
  gap: 12px;

  .spinner {
    width: 40px;
    height: 40px;
    border-radius: 100%;
    background-color: aqua;
    display: grid;
    place-items: center;
    animation: zoomin 1.5s infinite alternate-reverse;
    position: relative;
  }

  .inner {
    background-color: #000000ff;
    width: 80%;
    height: 80%;
    border-radius: 100%;
  }

  /* Texte des étapes avec gradient animé */
  .message {
    font-size: 0.95rem;
    margin-top: 10px;
    text-align: center;

    /* --- gradient animé (tutoriel) --- */
    background: linear-gradient(
      to right,
      #7953cd 20%,
      #00affa 30%,
      #0190cd 70%,
      #764ada 80%
      
    );
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-fill-color: transparent;
    background-size: 500% auto;
    animation: textShine 5s ease-in-out infinite alternate;
  }

  @keyframes zoomin {
    0% {
      transform: scale(1);
      box-shadow: 0 0 100px 20px rgba(23, 124, 124, 1);
    }
    100% {
      transform: scale(1.5);
      box-shadow: 0 0 100px 20px rgba(14, 68, 68, 1);
    }
  }

  @keyframes textShine {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 100% 50%;
    }
  }
`;

export default Loader;
