import React from "react";

const FormatText = ({ text }) => {
  const lines = text.split(/\n/);
  return (
    <div>
      {lines.map((line, index) => (
        <p key={index}>{line}</p>
      ))}
    </div>
  );
};

export default FormatText;
