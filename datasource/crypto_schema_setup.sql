CREATE TABLE IF NOT EXISTS details (
            cryptoId INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            name TEXT NOT NULL,
            symbol TEXT NOT NULL,
            supply REAL,
            maxSupply REAL,
            marketCapUsd REAL,
            volumeUsd24Hr REAL,
            priceUsd REAL,
            changePercent24Hr REAL,
            vwap24Hr REAL,
            explorer TEXT
);


CREATE TABLE IF NOT EXISTS historic_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptoId INTEGER,
            priceUsd REAL,
            date DATE,
            FOREIGN KEY (cryptoId) REFERENCES crypto_info(id)
);


CREATE TABLE IF NOT EXISTS markets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptoId INTEGER,
            exchangeId TEXT,
            quoteId TEXT,
            baseSymbol TEXT,
            quoteSymbol TEXT,
            volumeUsd24Hr REAL,
            priceUsd REAL,
            volumePercent REAL,
            FOREIGN KEY (cryptoId) REFERENCES crypto_info(id)
);


CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptoId INTEGER,
            title TEXT,
            media TEXT,
            news_date TEXT,
            description TEXT,
            link TEXT,
            FOREIGN KEY (cryptoId) REFERENCES crypto_info(id)
);