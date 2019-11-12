CREATE TABLE frequency (
                        octave INTEGER NOT NULL  PRIMARY KEY,
                        C float,
                        CSharp float,
                        D float,
                        DSharp float,
                        E float,
                        F float,
                        FSharp float,
                        G float,
                        GSharp float,
                        A      float,
                        ASharp float,
                        B float
);


INSERT INTO frequency VALUES(-1,16.351597831287414,17.323914436054505,18.354047994837973,19.445436482630058,20.60172230705437,21.826764464562743,23.12465141947715,24.49971474885933,25.95654359874657,27.5,29.13523509488062,30.867706328507758);
SELECT A
FROM frequency
WHERE octave=-1

