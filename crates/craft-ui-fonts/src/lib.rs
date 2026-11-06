//! Public OFL font bytes, with no UI framework or private repository dependency.
#![forbid(unsafe_code)]
#![deny(
    clippy::unwrap_used,
    clippy::expect_used,
    clippy::panic,
    clippy::unimplemented,
    clippy::todo,
    clippy::unreachable
)]
pub const DISPLAY: &[u8] =
    include_bytes!("../../../fonts/source-serif/SourceSerif4Display-Semibold.ttf");
pub const NUMERIC: &[u8] = include_bytes!("../../../fonts/inter-tabular/InterTabular-Regular.ttf");
pub const NUMERIC_SEMIBOLD: &[u8] =
    include_bytes!("../../../fonts/inter-tabular/InterTabular-SemiBold.ttf");

#[cfg(test)]
mod tests {
    #[test]
    fn fonts_parse_and_numeric_digits_have_equal_advances() {
        ttf_parser::Face::parse(super::DISPLAY, 0).unwrap();
        for bytes in [super::NUMERIC, super::NUMERIC_SEMIBOLD] {
            let face = ttf_parser::Face::parse(bytes, 0).unwrap();
            let widths: Vec<_> = "0123456789"
                .chars()
                .map(|c| {
                    face.glyph_hor_advance(face.glyph_index(c).unwrap())
                        .unwrap()
                })
                .collect();
            assert!(widths.iter().all(|width| *width == widths[0]));
        }
    }
}
