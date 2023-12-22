import React from "react";
import Link from "next/link";

const PrivacyPolicy = () => {
  return (
    <div className="container mx-auto px-10 py-10 text-gray-500">
      <h1 className="text-3xl font-bold underline text-center mb-6 text-[var(--primary-colour)]">
        Privacy Policy
      </h1>
      <section className="mb-6">
        <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
          Data Collection
        </h2>
        <p className="text-base">
          We collect various types of information for various purposes to
          provide and improve our service to you.
        </p>
        <ul className="list-disc pl-5">
          <li>
            Personal Data: While using our Service, we may ask you to provide us
            with certain personally identifiable information that can be used to
            contact or identify you .
          </li>
          <li>
            Usage Data: We may also collect information on how the Service is
            accessed and used .
          </li>
          <li>
            Tracking & Cookies Data: We use cookies and similar tracking
            technologies to track the activity on our Service and we hold
            certain information.
          </li>
        </ul>
      </section>
      <section className="mb-6">
        <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
          Use of Data
        </h2>
        <p className="text-base">
          XAICompanions uses the collected data for various purposes:
        </p>
        <ul className="list-disc pl-5">
          <li>To provide and maintain our Service</li>
          <li>To notify you about changes to our Service</li>
          <li>
            To allow you to participate in interactive features of our Service
            when you choose to do so
          </li>
          <li>To provide customer support</li>
          <li>
            To gather analysis or valuable information so that we can improve
            our Service
          </li>
          <li>To monitor the usage of our Service</li>
          <li>To detect, prevent and address technical issues</li>
        </ul>
      </section>
      <section className="mb-6">
        <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
          Data Protection
        </h2>
        <p className="text-base">
          The security of your data is important to us but remember that no
          method of transmission over the Internet or method of electronic
          storage is 100% secure. While we strive to use commercially acceptable
          means to protect your Personal Data, we cannot guarantee its absolute
          security.
        </p>
      </section>
      <section className="mb-6">
        <h2 className="text-2xl font-bold mb-4 text-[var(--primary-colour)]">
          Contact Us
        </h2>
        <p className="text-base r">
          If you have any questions about this Privacy Policy, please contact us
          through our email.
          <div className="flex items-center">
            <span>Email :-</span>
            <Link
              rel="noopener noreferrer"
              href="mailto:xaicompanions@gmail.com"
              title="Email"
              className="inline-flex ml-2 items-center justify-center w-10 h-10 rounded-full bg-gray-100 text-gray-900 hover:scale-[1.02]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
                className="w-5 h-5"
              >
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path>
              </svg>
            </Link>
          </div>
        </p>
      </section>
    </div>
  );
};

export default PrivacyPolicy;
