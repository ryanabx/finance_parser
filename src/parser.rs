use std::num::ParseFloatError;

use chrono::{NaiveDate, ParseError};
use csv::StringRecord;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum EntryParseError {
    #[error("Record not found: {0}")]
    RecordNotFound(String),
    #[error("Parsing date time failed: {0}")]
    DateTimeParse(#[from] ParseError),
    #[error("Parsing cost failed: {0}")]
    FloatParse(#[from] ParseFloatError),
}

#[derive(Debug, Clone)]
pub struct Entry {
    pub cost: f32,
    pub date: NaiveDate,
    pub from_source: String,
    pub description: String,
}

impl Entry {
    pub fn new(record: StringRecord) -> Result<Self, EntryParseError> {
        Ok(Entry {
            cost: parse_cost(
                record
                    .get(0)
                    .ok_or(EntryParseError::RecordNotFound("Cost".to_string()))?,
            )?,
            from_source: record
                .get(1)
                .ok_or(EntryParseError::RecordNotFound("Source".to_string()))?
                .to_string(),
            date: parse_date(
                record
                    .get(2)
                    .ok_or(EntryParseError::RecordNotFound("Date".to_string()))?,
            )?,
            description: record
                .get(3)
                .ok_or(EntryParseError::RecordNotFound("Description".to_string()))?
                .to_string(),
        })
    }
}

fn parse_date(date: &str) -> Result<NaiveDate, EntryParseError> {
    log::trace!("Date: {}", date);
    Ok(NaiveDate::parse_from_str(date, "%m/%d/%y")?)
}

fn parse_cost(cost: &str) -> Result<f32, EntryParseError> {
    let mut formatted_cost = cost.replace("$", "");
    formatted_cost = formatted_cost.replace(",", "");
    log::trace!("Cost: {} -> {}", cost, formatted_cost);
    Ok(formatted_cost.parse::<f32>()?)
}
