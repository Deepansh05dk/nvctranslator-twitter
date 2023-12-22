import React from "react";
import Image from "next/image";

const About = () => {
  return (
    <div className="p-5 sm:p-10 md:p-16 ">
      <div className="flex flex-col mx-auto container overflow-hidden rounded ">
        <Image
          src="/about.png"
          alt="about"
          className="w-full h-[40vh] sm:h-[60vh]"
          width={1792}
          height={1024}
        />
        <div className="p-6 pb-12 m-4 mx-auto -mt-16 space-y-6  sm:px-10 sm:mx-12 lg:rounded-md bg-white shadow-md font-sans">
          <div className=" p-8 text-gray-500">
            <div className="container mx-auto">
              <h1 className="text-3xl font-bold text-center my-10 text-[var(--primary-colour)]">
                About Us
              </h1>
              <p className="text-md sm:text-lg mb-8">
                Welcome to XAICompanion, where we bring clarity, sophistication,
                and empathy to the Twitterverse! Our innovative platform hosts a
                family of specialized AI bots designed to enhance your tweeting
                experience, making communication on Twitter not just easier, but
                more meaningful and impactful.
              </p>

              <section className="mb-10">
                <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
                  Our Vision:
                </h2>
                <p className="text-md sm:text-lg ">
                  In the fast-paced world of social media, clarity and
                  understanding often take a backseat. XAICompanion is here to
                  change that. Our vision is to empower every Twitter user with
                  the ability to express and absorb information effectively, no
                  matter the complexity or context.
                </p>
              </section>

              <section className="mb-10">
                <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
                  What We Do:
                </h2>
                <p className="text-md sm:text-lg ">
                  XAICompanion offers a range of AI-powered bots, each tailored
                  for specific communication needs on Twitter. From simplifying
                  complex topics into child-friendly explanations to elevating
                  casual tweets into formal prose, our bots work tirelessly to
                  translate, transform, and transcend language barriers. Our
                  bots are not just translators but companions in your digital
                  communication journey.
                </p>
              </section>

              <section className="my-10">
                <h2 className="text-2xl font-bold mb-4 text-left text-[var(--primary-colour)]">
                  Why Choose XAICompanion?
                </h2>
                <div className="space-y-4">
                  <div className="flex items-start">
                    <div className="text-teal-500">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 mr-2"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[var(--primary-colour)]">
                        User-Centric Design
                      </h3>
                      <p className="text-md sm:text-lg ">
                        Our bots are crafted with the end-user in mind, ensuring
                        an intuitive, helpful, and delightful experience.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <div className="text-teal-500">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 mr-2"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[var(--primary-colour)]">
                        Quality Translations
                      </h3>
                      <p className="text-md sm:text-lg ">
                        {
                          "We pride ourselves on accurate, context-aware translations that preserve the original intent and tone."
                        }
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <div className="text-teal-500">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 mr-2"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-[var(--primary-colour)]">
                        Diverse Range
                      </h3>
                      <p className="text-md sm:text-lg ">
                        {
                          " Whether you're a student, professional, or just looking for clearer communication, our bots cater to a wide spectrum of needs."
                        }
                      </p>
                    </div>
                  </div>
                </div>
              </section>

              <section className="mb-10">
                <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
                  Join Our Community:
                </h2>
                <p className="text-md sm:text-lg ">
                  Become part of a growing community dedicated to better,
                  clearer, and more empathetic communication on Twitter. Try out
                  our bots, see the difference they make, and let us know your
                  thoughts! For the latest updates, follow us on Twitter and
                  join our user group.
                </p>
              </section>

              <section className="mt-8">
                <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
                  Contact Us:
                </h2>
                <p className="text-md sm:text-lg">
                  {
                    "We're always here to help or hear from you! For support, feedback,or inquiries, email us."
                  }
                </p>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
