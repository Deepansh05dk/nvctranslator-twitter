import React from "react";

const Divider = ({ text }) => {
  return (
    <span className="relative flex justify-center mt-10">
      <div className="absolute inset-x-0 top-1/2 h-px -translate-y-1/2 bg-transparent bg-gradient-to-r from-transparent via-[var(--primary-colour)] to-transparent opacity-75"></div>
      <span className="relative z-10 bg-[var(--primary-colour)]  text-white text-lg sm:text-xl px-6 py-2">
        {text}
      </span>
    </span>
  );
};

export default Divider;
