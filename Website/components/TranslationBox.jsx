import React, { useState } from "react";
import Image from "next/image";
import FormatText from "./FormatText";
import Link from "next/link";
import Navbar from "./SecondaryNavbar";

export const TranslationBox = ({
  tweet,
  theme,
  userData,
  botProperties,
  botname,
}) => {
  const [translated, setTranslated] = useState(true);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const handleCopyClick = () => {
    navigator.clipboard
      .writeText(document.getElementById("textBox").innerText)
      .then(() => {
        setNotificationVisible(true); // Show notification
        setTimeout(() => {
          setNotificationVisible(false); // Hide notification after 3 seconds
        }, 3000);
      })
      .catch((err) => console.error("Error copying text: ", err));
  };

  return (
    <>
      <div className="rounded-md bg-white font-normal shadow-md ">
        <Navbar
          title={botProperties.title}
          theme={botProperties.themeColor}
          logo_url={botProperties.logo}
          botname={botname}
        ></Navbar>
        <div className="flex flex-row w-full items-center space-x-4 py-5 px-6">
          <div>
            <Image
              src={userData.profile_image_url}
              alt="logo"
              className="rounded-full"
              height={60}
              width={60}
            />
          </div>
          <Link
            className="flex flex-col items-start"
            href={`https://twitter.com/${userData.username}`}
          >
            <div className="font-semibold  text-base sm:text-lg">
              {userData.name.slice(0, 30) +
                (userData.name.length > 30 ? "..." : "")}
            </div>
            <div className="font-extralight text-sm">@{userData.username}</div>
          </Link>
        </div>
        <div className="flex flex-col-reverse lg:justify-between lg:flex-row lg:items-baseline px-8 lg:px-10">
          <div id="textBox" className="my-6 lg:mr-4">
            {translated ? (
              <FormatText
                text={tweet.translated_text.replaceAll("<<>>", " ")}
              />
            ) : (
              <FormatText text={tweet.original_text} />
            )}
          </div>
          <div className="inline-flex mx-auto rounded-lg border border-gray-100 bg-gray-100 p-1 mb-4 lg:mx-0">
            <button
              type="button"
              onClick={() => setTranslated(!translated)}
              className={
                "inline-block font-medium rounded-md px-4 py-2 text-sm focus:relative " +
                (translated
                  ? `${theme} shadow-sm text-white`
                  : "text-gray-500 hover:text-gray-700")
              }
            >
              {botname === "makethismature" ? "MoreMature" : "Translated"}
            </button>
            <button
              type="button"
              onClick={() => setTranslated(!translated)}
              className={
                "inline-block font-medium rounded-md px-4 py-2 text-sm focus:relative  " +
                (translated
                  ? "text-gray-500 hover:text-gray-700"
                  : `${theme} shadow-sm text-white`)
              }
            >
              Original
            </button>
          </div>
        </div>

        <div className="text-center">
          <button
            type="button"
            id="copyButton"
            onClick={handleCopyClick}
            className={`px-4 py-2 my-5 font-medium rounded-md ${theme} text-white hover:scale-[1.02]`}
          >
            Copy
          </button>
        </div>

        <div
          id="notification"
          className={
            "fixed top-4 left-1/2  transform -translate-x-1/2 bg-white text-[#316382] z-20 py-2 px-4 rounded-lg" +
            (notificationVisible ? "" : " hidden")
          }
        >
          Copied!
        </div>
      </div>
    </>
  );
};
