import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI;

if (!uri) {
  throw new Error("Please add your Mongo URI to .env.local");
}

let client;
let clientPromise;

try {
  if (process.env.NODE_ENV === "development") {
    // In development mode, use a global variable for caching the client
    if (!global._mongoClientPromise) {
      client = new MongoClient(uri);
      global._mongoClientPromise = client.connect();
    }
    clientPromise = global._mongoClientPromise;
  } else {
    // In production mode, use a new client instance
    client = new MongoClient(uri);
    clientPromise = client.connect();
  }
} catch (error) {
  console.error("MongoDB connection error:", error);
  throw error; // Re-throwing the error to handle it at a higher level
}

export default clientPromise;
