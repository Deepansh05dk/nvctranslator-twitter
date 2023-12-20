import React from "react";
import Image from "next/image";
import Link from "next/link";

const Footer = () => {
  return (
    <footer className="bg-[#316382] text-white ">
      <div className="mx-auto max-w-screen-xl px-2 py-4 sm:py-6 sm:px-4 lg:px-8">
        <div className="sm:flex sm:items-center sm:justify-between">
          <div className="flex-row space-x-10 flex items-center justify-center">
            <div className="font-medium text-center">
              <Image
                src={"/logos/main.jpeg"}
                className=" text-white rounded-full bg-white inline"
                alt="logo"
                width={30}
                height={30}
              />{" "}
              XAICompanions
            </div>
            <Link className="mr-10" href="/privacy-policy">
              Privacy Policy
            </Link>
          </div>

          <div className="items-center text-sm sm:text-base">
            <p className="text-center text-sm  lg:mt-0 lg:text-right">
              Copyright &copy; 2023. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
