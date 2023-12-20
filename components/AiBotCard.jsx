import React from "react";
import Image from "next/image";
import Link from "next/link";

const AiBotCard = ({ bot }) => {
  return (
    <Link
      href={bot.twitterLink}
      className="group relative block bg-black w-[90vw] sm:w-[40vw] lg:w-[25vw] xl:w-[20vw] h-72 m-5 "
    >
      <Image
        alt="Developer"
        src={bot.logo}
        className="absolute inset-0 h-full w-full object-cover opacity-70 transition-opacity group-hover:opacity-50"
        width={400}
        height={258}
      />

      <div className="relative p-4 sm:p-6 lg:p-8">
        <p className="text-xl font-bold text-[white] sm:text-2xl">{bot.name}</p>
        <div className="mt-20">
          <div className="translate-y-8 transform opacity-0 transition-all group-hover:translate-y-0 group-hover:opacity-100">
            <p className="text-xl text-white">{bot.description}</p>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default AiBotCard;
