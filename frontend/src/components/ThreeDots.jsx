import React from 'react';

const ThreeDots = ({ color = '#32cd32', size = 'medium', text = '', textColor = '' }) => {
  const dotSize = size === 'small' ? 6 : size === 'large' ? 14 : 10;
  const textStyle = { color: textColor || color, marginLeft: '8px' };

  return (
    <div style={{ display: 'flex', alignItems: 'center' }}>
      <div style={{ display: 'flex', gap: '4px' }}>
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            style={{
              width: dotSize,
              height: dotSize,
              borderRadius: '50%',
              backgroundColor: color,
              animation: `blink 1.4s infinite both`,
              animationDelay: `${i * 0.2}s`,
            }}
          ></div>
        ))}
      </div>
      {text && <span style={textStyle}>{text}</span>}
      <style>{`
        @keyframes blink {
          0%, 80%, 100% { opacity: 0; }
          40% { opacity: 1; }
        }
      `}</style>
    </div>
  );
};

export default ThreeDots;
