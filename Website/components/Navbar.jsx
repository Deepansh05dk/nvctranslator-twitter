import React from "react";
import Link from "next/link";
import Image from "next/image";

const Navbar = () => {
  return (
    <header className="text-white body-font sticky top-0 z-20 bg-[#316382] ">
      <div className="container mx-auto flex sm:flex-row px-6 py-[10px] sm:py-3 flex-row items-center justify-between ">
        <Link
          className="flex title-font font-medium items-center  md:mb-0"
          href={"/"}
        >
          <Image
            src={"/logos/main.jpeg"}
            className=" rounded-full bg-white"
            alt="logo"
            width={50}
            height={50}
          />
          <span className="ml-3 text-base sm:text-xl">XAICompanions</span>
        </Link>
        {/* <button className="inline-flex items-center bg-[#316382] border-0 py-1 px-3 focus:outline-none hover:bg-gray-200 rounded text-sm sm:text-base md:mt-0">
          Try our Bots
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
        </button> */}
      </div>
    </header>
  );
};

export default Navbar;
