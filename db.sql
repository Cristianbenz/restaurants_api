CREATE TABLE restaurants (
    id TEXT PRIMARY KEY NOT NULL,
    rating INTEGER CHECK (rating >= 0 AND rating <= 4) NOT NULL,
    name TEXT NOT NULL,
    site TEXT,
    email TEXT,
    phone TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    lat REAL NOT NULL,
    lng REAL NOT NULL
);