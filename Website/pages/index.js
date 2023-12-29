import AiBotCard from "../components/AiBotCard";
import Image from "next/image";
import Link from "next/link";
import Divider from "../components/Divider";

export default function Home() {
  return (
    <div className="min-h-screen">
      <main>
        <section className="relative bg-custom bg-cover bg-blend-hard-light bg-center bg-no-repeat min-h-[80vh] fadeIn max-h-[90vh] ">
          <div className="absolute inset-0 bg-transparent from-[#c3c6c7] bg-gradient-to-r "></div>
          <div className="relative mx-auto max-w-screen-xl px-4 py-32 sm:px-6 lg:flex lg:h-screen lg:items-center lg:px-8">
            <div className="max-w-3xl  sm:text-left px-10">
              <h1 className="text-3xl font-extrabold sm:text-5xl ">
                Crafting Your Ideal Twitter Experience
              </h1>

              <p className="mt-4 font-semibold max-w-xl sm:text-2xl/relaxed">
                Where AI Meets Tweeting – Crafting Smarter Conversations for the
                Digital Age.
              </p>

              <div className="mt-8 flex flex-wrap gap-4 text-center ">
                <Link
                  href="#bots"
                  className="flex  justify-center rounded bg-[var(--primary-colour)] px-12 py-3 sm:text-sm text-xs font-medium text-white shadow hover:scale-[1.02] focus:outline-none sm:w-auto"
                >
                  Explore Our Bots
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

                <Link
                  href="#demo"
                  className="flex  justify-center rounded bg-white px-12 py-3 sm:text-sm text-xs font-medium text-[var(--primary-colour)] shadow hover:scale-[1.02] focus:outline-none sm:w-auto"
                >
                  Demo
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
            </div>
          </div>
        </section>
        <Divider text={"Demo"} />
        <section id="demo" className="flex justify-center ">
          <div className="overflow-hidden  lg:grid lg:grid-cols-2 my-10 max-w-screen-xl">
            <div className="flex justify-center items-center p-8">
              <Image
                alt="demo"
                src="/demo.jpg"
                className="object-cover "
                width={600}
                height={600}
              />
            </div>
            <div className="p-4 md:p-8">
              <div className="max-w-2xl mx-auto my-8 p-4 text-[var(--primary-colour)]">
                <h2 className="text-2xl lg:text-3xl font-bold mb-4">
                  How to Use Our Twitter AI Bots
                </h2>
                <ol className="list-decimal list-inside">
                  <li className="mb-4 flex">
                    <div className="flex items-center justify-center flex-shrink-0 w-10 h-10 text-xl font-bold rounded-full bg-[var(--primary-colour)] text-white mr-3">
                      1
                    </div>
                    <div className="lg:text-lg">
                      <span>
                        Begin by following our AI bots on Twitter. Find them at
                        their respective handles, like{" "}
                      </span>
                      <span className="text-blue-400 font-semibold">
                        @eli5translator
                      </span>
                      <span>
                        . This step ensures you can easily interact with them
                        and stay updated with their latest responses and
                        features.
                      </span>
                    </div>
                  </li>
                  <li className="mb-4 flex">
                    <div className="flex items-center justify-center flex-shrink-0 w-10 h-10 text-xl font-bold rounded-full bg-[var(--primary-colour)] text-white mr-3">
                      2
                    </div>
                    <div className="lg:text-lg">
                      <span>
                        To interact with the bot, simply tag it in a reply to
                        any tweet. For instance, reply to a tweet and include{" "}
                      </span>
                      <span className="text-blue-400 font-semibold">
                        @eli5translator
                      </span>
                      <span>
                        {" "}
                        in your message. This action signals our bot to engage
                        with your tweet.
                      </span>
                    </div>
                  </li>
                  <li className="flex">
                    <div className="flex items-center justify-center flex-shrink-0 w-10 h-10 text-xl font-bold rounded-full bg-[var(--primary-colour)] text-white mr-3">
                      3
                    </div>
                    <span className="lg:text-lg">
                      After tagging our bot, wait for a swift reply. Our AI bots
                      are programmed to respond quickly, offering insightful,
                      witty, or helpful responses based on the context of the
                      tweet.
                    </span>
                  </li>
                </ol>
              </div>
            </div>
          </div>
        </section>
        <Divider text={"Bots"} />
        <section
          id="bots"
          className="flex justify-center items-center flex-wrap my-20 sm:px-5 lg:px-10 "
        >
          {bots.map((bot) => (
            <AiBotCard key={bot.name} bot={bot} />
          ))}
        </section>
      </main>
    </div>
  );
}

const bots = [
  // Add your bots here. Each bot should have a name, description, and Twitter link
  {
    name: "NVCTranslator",
    description:
      "Translate any tweet text to NVC, Marshall Rosenberg's Nonviolent Communication",
    logo: "/logos/nvctranslator.jpg",
    twitterLink: "https://twitter.com/nvctranslator",
  },
  {
    name: "ELI5Translator",
    description:
      "Simplify complex tweets into easy-to-understand explanations, as if explaining to a five-year-old",
    logo: "/logos/eli5translator.png",
    twitterLink: "https://twitter.com/eli5translator",
  },
  {
    name: "AdultTranslate",
    description:
      "Transforming casual tweets into polished, formal English. Your go-to for elevating everyday slang to articulate expressions",
    logo: "/logos/adulttranslate.png",
    twitterLink: "https://twitter.com/adulttranslate",
  },
  {
    name: "MakeThisMature",
    description:
      " From simple to sophisticated: Elevating tweets into polished prose . Ideal for academic and professional use",
    logo: "/logos/makethismature.png",
    twitterLink: "https://twitter.com/makethismature",
  },
  // More bots...
];
