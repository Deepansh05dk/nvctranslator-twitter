import React from "react";
import Image from "next/image";
import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-[#316382] text-white ">
      <div className="mx-auto max-w-screen-xl px-2 py-4  sm:px-4 lg:px-8">
        <div className="sm:flex sm:items-center sm:justify-between">
          <div className="flex-row space-x-10 flex items-center justify-center text-xs sm:text-sm mb-3 sm:mb-0 ">
            <div className=" text-center flex items-center ">
              <Image
                src={"/logos/main.jpeg"}
                className=" text-white rounded-full bg-white inline"
                alt="logo"
                width={35}
                height={35}
              />
              <span className="ml-2">XAICompanions</span>
            </div>
            <Link className="mr-10 text-white/70" href="/privacy-policy">
              Privacy Policy
            </Link>
          </div>

          <div className="items-center">
            <p className="text-center text-xs sm:text-sm  lg:mt-0 lg:text-right">
              Copyright &copy; 2023. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
