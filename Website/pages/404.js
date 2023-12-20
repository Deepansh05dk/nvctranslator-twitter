import Link from "next/link";

export default function FourOhFour() {
  return (
    <section className="flex items-center h-full p-16  text-[#316382] min-h-[85vh]">
      <div className="container flex flex-col items-center justify-center px-5 mx-auto my-8">
        <div className="max-w-md text-center">
          <h2 className="mb-8 font-extrabold text-9xl text-gray-600">
            <span className="sr-only">Error</span>404
          </h2>
          <p className="text-2xl font-semibold md:text-3xl">
            {"Sorry, we couldn't find this page."}
          </p>
          <p className="mt-4 mb-8 text-gray-400">
            But dont worry, you can find plenty of other things on our homepage.
          </p>
          <Link
            rel="noopener noreferrer"
            href="/"
            className="px-8 py-3 font-semibold rounded bg-[#316382] hover:bg-[#316382]/80 text-white"
          >
            Back to homepage
          </Link>
        </div>
      </div>
    </section>
  );
}
