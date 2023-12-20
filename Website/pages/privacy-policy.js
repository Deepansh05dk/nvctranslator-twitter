import React from "react";

const PrivacyPolicy = () => {
  return (
    <div className="container mx-auto px-10 py-10 text-[#316382]">
      <h1 className="text-3xl font-bold underline text-center my-6 text-[#233d4d]">
        Privacy Policy
      </h1>
      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-[#233d4d]">
          Data Collection
        </h2>
        <p className="text-lg">
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
        <h2 className="text-2xl font-semibold mb-4 text-[#233d4d]">
          Use of Data
        </h2>
        <p className="text-lg">
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
        <h2 className="text-2xl font-semibold mb-4 text-[#233d4d]">
          Data Protection
        </h2>
        <p className="text-lg">
          The security of your data is important to us but remember that no
          method of transmission over the Internet or method of electronic
          storage is 100% secure. While we strive to use commercially acceptable
          means to protect your Personal Data, we cannot guarantee its absolute
          security.
        </p>
      </section>
      <section className="mb-6">
        <h2 className="text-2xl font-semibold mb-4 text-[#233d4d]">
          Contact Us
        </h2>
        <p className="text-lg">
          If you have any questions about this Privacy Policy, please contact
          us.
        </p>
      </section>
    </div>
  );
};

export default PrivacyPolicy;
