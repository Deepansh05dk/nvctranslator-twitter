import "@/styles/globals.css";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import Head from "next/head";

export default function App({ Component, pageProps }) {
  return (
    <>
      <Head>
        <title>XAICompanions</title>
        <link
          rel="shortcut icon"
          href={"/logos/main.png"}
          type="image/x-icon"
        />
      </Head>
      <Navbar />
      <Component {...pageProps} />
      <Footer />
    </>
  );
}
