use std::io;

use parser::EntryParseError;
use thiserror::Error;

mod parser;

#[derive(Debug, Error)]
enum FinanceParserError {
    #[error("Entry parse: {0}")]
    Parser(#[from] EntryParseError),
    #[error("CSV: {0}")]
    Csv(#[from] csv::Error),
}

fn main() -> anyhow::Result<()> {
    env_logger::init();
    let mut rdr = csv::ReaderBuilder::new()
        .has_headers(false)
        .delimiter(b'\t')
        .from_reader(io::stdin());
    let parsed_record = rdr
        .records()
        .map(|record| {
            record
                .map_err(FinanceParserError::Csv)
                .and_then(|x| parser::Entry::new(x).map_err(FinanceParserError::Parser))
        })
        .collect::<Result<Vec<_>, FinanceParserError>>();
    for result in parsed_record? {
        println!("{:?}", result);
    }
    println!("Hello, world!");
    Ok(())
}
