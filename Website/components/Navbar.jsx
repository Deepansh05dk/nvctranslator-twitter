import React from "react";
import Link from "next/link";
import Image from "next/image";

const Navbar = () => {
  return (
    <header className="text-white body-font sticky top-0 z-20 bg-[var(--primary-colour)] ">
      <div className="container mx-auto flex sm:flex-row px-6 py-[10px] sm:py-3 flex-row items-center justify-between ">
        <Link
          className="flex title-font font-medium items-center  md:mb-0"
          href={"/"}
        >
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-white">
            <Image
              src={"/logos/main.png"}
              className=" text-white rounded-full bg-white inline"
              alt="logo"
              width={35}
              height={35}
            />
          </div>
          <span className="ml-3 text-base sm:text-xl">XAICompanions</span>
        </Link>
        <Link
          href="/about"
          className="inline-flex items-center text-[var(--primary-colour)] bg-white border-0 py-1 px-3 focus:outline-none rounded text-sm sm:text-base font-medium hover:scale-[1.02]"
        >
          About Us
          <svg
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="w-4 h-4 ml-1"
            viewBox="0 0 24 24"
          >
            <path d="M5 12h14M12 5l7 7-7 7"></path>
          </svg>
        </Link>
      </div>
    </header>
  );
};

export default Navbar;
