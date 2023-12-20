import React from "react";
import Image from "next/image";
import Link from "next/link";

const Navbar = ({ title, theme, logo_url, botname }) => {
  return (
    <header className={theme + " rounded-t-md"}>
      <div
        className={
          "container mx-auto flex flex-wrap py-3 flex-col md:flex-row items-center justify-between px-6 text-white"
        }
      >
        <Link
          className="flex title-font font-bold items-center "
          href={`https://twitter.com/${botname}`}
        >
          <Image
            src={logo_url}
            className=" text-white rounded-full bg-white"
            alt="logo"
            width={50}
            height={50}
          />
          <span className="ml-3 text-lg">{title}</span>
        </Link>
      </div>
    </header>
  );
};

export default Navbar;
