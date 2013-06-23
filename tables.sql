BEGIN;

CREATE TABLE ultimate_ox_profiles (
    "user" INTEGER NOT NULL,
    preferred_colour INTEGER,
    preferred_opponent INTEGER,
    PRIMARY KEY ("user"),
    FOREIGN KEY("user") REFERENCES users (id)
);
CREATE INDEX ix_ultimate_ox_profiles_user ON ultimate_ox_profiles ("user");

CREATE TABLE ultimate_ox_games (
    id SERIAL NOT NULL,
    turn INTEGER,
    started TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    player1 INTEGER NOT NULL,
    player2 INTEGER NOT NULL,
    winner INTEGER,
    overall_state VARCHAR NOT NULL,
    current_state VARCHAR NOT NULL,
    active_board INTEGER NOT NULL,
    rematch INTEGER,
    source INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(player1) REFERENCES users (id),
    FOREIGN KEY(player2) REFERENCES users (id),
    FOREIGN KEY(winner) REFERENCES users (id),
    FOREIGN KEY(rematch) REFERENCES ultimate_ox_games (id),
    FOREIGN KEY(source) REFERENCES ultimate_ox_games (id)
);
CREATE INDEX ix_ultimate_ox_games_player2 ON ultimate_ox_games (player2);
CREATE INDEX ix_ultimate_ox_games_player1 ON ultimate_ox_games (player1);

CREATE TABLE ultimate_ox_moves (
    id SERIAL NOT NULL,
    game INTEGER NOT NULL,
    player INTEGER NOT NULL,
    move INTEGER NOT NULL,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(game) REFERENCES ultimate_ox_games (id),
    FOREIGN KEY(player) REFERENCES users (id)
);
CREATE INDEX ix_ultimate_ox_moves_player ON ultimate_ox_moves (player);

COMMIT;