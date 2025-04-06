use serde::{Deserialize, Serialize};

// preprocessing strategies
pub trait Normalize {
    fn normalize(&self, text: &mut String);
}

/// trim whitespace normalizer
pub struct DefaultNormalizer;

impl DefaultNormalizer {
    fn is_whitespace(&self, c: u8) -> bool {
        c == b' ' || c == b'\t'
    }
}

impl Normalize for DefaultNormalizer {
    // https://stackoverflow.com/questions/71864137/whats-the-ideal-way-to-trim-extra-spaces-from-a-string
    fn normalize(&self, text: &mut String) {
        let mut prev = ' ';
        text.retain(|x| {
            let res = !self.is_whitespace(x as u8) || !self.is_whitespace(prev as u8);
            prev = x;
            res
        });
    }
}

// hack
#[derive(Serialize, Deserialize, Debug, PartialEq, Clone)]
#[derive(Default)]
pub enum Normalizer {
    #[default]
    WhitespaceOnly,
}

impl Normalizer {
    pub fn into_strategy(&self) -> Box<dyn Normalize + Send + Sync> {
        match &self {
            Normalizer::WhitespaceOnly => Box::new(DefaultNormalizer),
        }
    }
}

