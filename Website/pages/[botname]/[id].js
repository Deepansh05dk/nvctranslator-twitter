import clientPromise from "@/database/mongodb";
import Link from "next/link";
import Head from "next/head";
import { useRouter } from "next/router";
import { TranslationBox } from "@/components/TranslationBox.jsx";
import Error from "@/components/Error";
import Divider from "@/components/Divider";
import axios from "axios";
import Image from "next/image";
import FormatText from "@/components/FormatText";

export default function TweetPage({ tweet, error, userData, relatedTweets }) {
  const router = useRouter();
  const botProperties = getBotProperties(router.query.botname);
  return (
    <>
      {(error === "tweet" || error === null) && (
        <div className="container px-5 py-4 md:py-7 mx-auto ">
          <Head>
            <title>{router.query.botname}</title>
            <link
              rel="shortcut icon"
              href={botProperties.logo}
              type="image/x-icon"
            />
          </Head>
          {error === "tweet" ? (
            <Error bot={router.query.botname} error={error} />
          ) : (
            <>
              <TranslationBox
                tweet={tweet}
                botProperties={botProperties}
                theme={botProperties.themeColor}
                botname={router.query.botname}
                userData={userData}
              />
              <div className="flex justify-end my-10">
                <Link
                  href="/"
                  className="flex w-full justify-center rounded bg-[#316382] px-12 py-3 text-sm font-medium text-white shadow hover:bg-[#316382]/80 focus:outline-none focus:ring sm:w-auto"
                >
                  Explore Our More AI Bots
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
              <Divider
                text={`More from ${
                  userData.name.slice(0, 21) +
                  (userData.name.length > 21 ? "..." : "")
                }`}
              />
              <section className="flex justify-center flex-wrap my-10">
                {relatedTweets.map((related_tweet) => {
                  return (
                    <div
                      onClick={() =>
                        router.push(
                          `/${router.query.botname}/${related_tweet.tweet_id}`
                        )
                      }
                      className=" cursor-pointer rounded-md h-96 border shadow-md w-80 m-5 transition-transform transform hover:scale-105 px-6 bg-white"
                      key={related_tweet.tweet_id}
                    >
                      <div className="flex flex-row w-full items-center space-x-4 py-5 ">
                        <div>
                          <Image
                            src={userData.profile_image_url}
                            alt="logo"
                            className="rounded-full"
                            height={50}
                            width={50}
                          />
                        </div>
                        <Link
                          className="flex flex-col items-start"
                          href={`https://twitter.com/${userData.username}`}
                        >
                          <div className="font-semibold text-sm sm:text-base">
                            {userData.name.slice(0, 20) +
                              (userData.name.length > 20 ? "..." : "")}
                          </div>
                          <div className="font-extralight text-xs">
                            @{userData.username}
                          </div>
                        </Link>
                      </div>
                      <FormatText
                        text={
                          related_tweet.translated_text
                            .slice(0, 360)
                            .replaceAll("<<>>", " ") +
                          (related_tweet.translated_text.length > 360
                            ? "..."
                            : "")
                        }
                      />
                    </div>
                  );
                })}
              </section>
            </>
          )}{" "}
        </div>
      )}
      {error === "bot" && <Error error={error} />}
    </>
  );
}

export async function getServerSideProps(context) {
  const { botname, id } = context.params;

  try {
    const client = await clientPromise;
    // Check if the database (bot) exists
    const dbs = await client.db().admin().listDatabases();
    const botExists = dbs.databases.some((db) => db.name === botname);
    if (!botExists) {
      // Bot does not exist
      return {
        props: { error: "bot" },
      };
    }
    const db = client.db(botname);
    const tweet = await db.collection("tweets").findOne({ tweet_id: id });
    const userId = tweet.userdetails_who_posted.id;
    const bearerToken = process.env.BEARER_TOKEN;
    const twitterApiResponse = await axios.get(
      `https://api.twitter.com/2/users/${userId}?user.fields=profile_image_url`,
      {
        headers: {
          Authorization: `Bearer ${bearerToken}`,
        },
      }
    );
    const userData = twitterApiResponse.data.data;
    const relatedTweets = await db
      .collection("tweets")
      .find({ "userdetails_who_posted.id": userId })
      .toArray();
    return {
      props: {
        userData: JSON.parse(JSON.stringify(userData)),
        tweet: JSON.parse(JSON.stringify(tweet)),
        relatedTweets: JSON.parse(JSON.stringify(relatedTweets)),
        error: null,
      },
    };
  } catch (err) {
    console.log("An error occurred while fetching data from MongoDB: ", err);
    return {
      props: { error: "tweet" },
    };
  }
}

const bots = {
  nvctranslator: {
    themeColor: "bg-[#fbbf24]",
    title: "NVCTranslator",
    logo: "/logos/nvctranslator.jpg",
  },
  eli5translator: {
    themeColor: "bg-[#68baa2]",
    title: "ELI5Translator",
    logo: "/logos/eli5translator.png",
  },
  adulttranslate: {
    themeColor: "bg-[#29558d]",
    title: "AdultTranslate",
    logo: "/logos/adulttranslate.png",
  },
  makethismature: {
    themeColor: "bg-[#ab551f]",
    title: "MakeThisMature",
    logo: "/logos/makethismature.png",
  },
};

function getBotProperties(botName) {
  if (!bots.hasOwnProperty(botName)) {
    return undefined;
  }
  return bots[botName];
}
