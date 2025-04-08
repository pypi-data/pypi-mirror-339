#import "utils.typ": *

#let default-font = state("font", none)
#let theme-color = state("theme-color", none)
#let background-color = state("background-color", _theme-colors.at("darky"))
#let sections = state("sections", ())
#let logo-img = state("logo", none)
#let alt-img = state("logo-alt", none)


//*************************************** Aux functions ***************************************\\

// LAIF colors

#let blue = _theme-colors.at("bluey")
#let darkblue = _theme-colors.at("darkbluey")
#let red = _theme-colors.at("reddy")
#let dusk = _theme-colors.at("darky")
#let darker = _theme-colors.at("darker")

#let bluey(body) = (text(fill: _theme-colors.at("bluey"))[#body])
#let darkbluey(body) = (text(fill: _theme-colors.at("darkbluey"))[#body])
#let reddy(body) = (text(fill: _theme-colors.at("reddy"))[#body])
#let dusky(body) = (text(fill: _theme-colors.at("darky"))[#body])
#let darker(body) = (text(fill: _theme-colors.at("darker"))[#body])

// Other

#let greeny(body) = (text(fill: _theme-colors.at("greeny"))[#body])
#let purply(body) = (text(fill: _theme-colors.at("purply"))[#body])
#let dusty(body) = (text(fill: _theme-colors.at("dusty"))[#body])
#let yelly(body) = (text(fill: _theme-colors.at("yelly"))[#body])


//***************************************************\\

#let stress(body) = (
  context {
    text(fill: theme-color.get(), weight: "semibold")[#body]
  }
)

//***************************************************\\

#let framed(
  title: none,
  back-color: none,
  content,
) = (
  context {
    let w = auto

    set block(
      inset: (x: .6cm, y: .6cm),
      breakable: false,
      above: .1cm,
      below: .1cm,
      width: 100%,
    )

    if title != none {
      stack(
        block(
          fill: theme-color.get(),
          inset: (x: .6cm, y: .55cm),
          radius: (top: .2cm, bottom: 0cm),
          stroke: 2pt,
        )[
          #text(weight: "semibold", fill: white)[#title]
        ],
        block(
          fill: {
            if back-color != none {
              back-color
            } else {
              white
            }
          },
          radius: (top: 0cm, bottom: .2cm),
          stroke: 2pt,
          content,
        ),
      )
    } else {
      stack(
        block(
          fill: if back-color != none {
            back-color
          } else {
            rgb("FBF7EE")
          },
          radius: (top: .2cm, bottom: .2cm),
          stroke: 2pt,
          content,
        ),
      )
    }
  }
)

//***************************************************\\

// Source: https://github.com/polylux-typ/polylux/blob/main/src/toolbox/toolbox-impl.typ

#let cols(columns: none, gutter: 1em, ..bodies) = {
  let bodies = bodies.pos()

  let columns = if columns == none {
    (1fr,) * bodies.len()
  } else {
    columns
  }

  if columns.len() != bodies.len() {
    panic("Number of columns must match number of content arguments")
  }

  grid(columns: columns, gutter: gutter, ..bodies)
}

//***************************************************\\

#let grayed(
  text-size: 24pt,
  content,
) = {
  set align(center + horizon)
  set text(size: text-size)
  block(
    fill: rgb("#F3F2F0"),
    inset: (x: .8cm, y: .8cm),
    breakable: false,
    above: .9cm,
    below: .9cm,
    radius: (top: .2cm, bottom: .2cm),
  )[#content]
}

//***************************************************\\

#let register-section(
  name,
) = (
  context {
    let sect-page = here().position()
    sections.update(sections => {
      sections.push((body: name, loc: sect-page))
      sections
    })
  }
)

//**************************************** Ending Slide ****************************************\\

#let ending-slide(
  text-color: white,
  text-size: 12pt,
  website-url: none,
  email: none,
) = (
  context {
    set page(fill: background-color.get())

    set text(
      weight: "semibold",
      size: text-size,
      fill: text-color,
      font: default-font.get(),
    )

    set align(center + horizon)


    v(5em)

    logo-img.get()

    v(7em)

    if website-url != none {
      _resize-text(link(website-url)[#text(fill: white)[#website-url.replace("https://", "")]])
    }
    if email != none {
      _resize-text(link("mailto:" + email)[#text(fill: blue)[#email]])
    }
  }
)

#let typslides(
  logo: text(""),
  logo-alt: text(""),
  website-url: none,
  email: none,
  ratio: "16-9",
  theme: "bluey",
  background: "darky",
  with-ending: true,
  font: "Fira Sans",
  body,
) = {
  theme-color.update(_theme-colors.at(theme))
  background-color.update(_theme-colors.at(background))
  logo-img.update(logo)
  alt-img.update(logo-alt)
  default-font.update(font)

  set text(font: font, fill: _theme-colors.at("darky"))
  set page(paper: "presentation-" + ratio, fill: white)

  show ref: it => (
    context {
      text(fill: theme-color.get())[#it]
    }
  )

  show link: it => (
    context {
      text(fill: theme-color.get())[#it]
    }
  )

  show footnote: it => (
    context {
      text(fill: theme-color.get())[#it]
    }
  )

  set enum(numbering: (it => context text(fill: background-color.get())[*#it.*]))

  body

  if with-ending {
    ending-slide(website-url: website-url, email: email)
  }
}

//**************************************** Front Slide ****************************************\\

#let front-slide(
  title: none,
  subtitle: none,
  authors: none,
  info: none,
) = (
  context {
    _make-frontpage(
      title,
      subtitle,
      authors,
      info,
      theme-color.get(),
      background-color.get(),
      logo-img.get(),
      alt-img.get(),
    )
  }
)

//*************************************** Content Slide ***************************************\\

#let table-of-contents(
  title: "Contents",
  text-size: 23pt,
) = (
  context {
    text(size: 42pt, weight: "bold")[
      #smallcaps(title)
      #v(-.9cm)
      #_divider(color: theme-color.get())
    ]

    set text(size: text-size)

    show linebreak: none

    let sections = sections.final()
    pad(enum(..sections.map(section => link(section.loc, section.body))))

    pagebreak()
  }
)

//**************************************** Title Slide ****************************************\\

#let title-slide(
  body,
  text-size: 42pt,
) = (
  context {
    register-section(body)

    show heading: text.with(size: text-size, weight: "semibold")

    set align(left + horizon)

    [= #smallcaps(body)]

    _divider(color: theme-color.get())

    pagebreak()
  }
)

// title-slide alias
#let section = title-slide

//**************************************** Focus Slide ****************************************\\

#let focus-slide(
  text-color: white,
  text-size: 36pt,
  body,
) = (
  context {
    set page(fill: theme-color.get())

    set text(
      weight: "semibold",
      size: text-size,
      fill: text-color,
      font: default-font.get(),
    )

    set align(center + horizon)

    _resize-text(body)
  }
)

//****************************************** Slide ********************************************\\

#let slide(
  title: none,
  back-color: white,
  body,
) = (
  context {
    let page-num = context counter(page).display(
      "1/1",
      both: true,
    )

    set page(
      fill: back-color,
      header-ascent: 65%,
      header: [
        #align(right)[
          #text(
            fill: white,
            weight: "semibold",
            size: 12pt,
          )[#page-num]
        ]
      ],
      margin: (x: 1.6cm, top: 2.5cm, bottom: 1.2cm),
      background: place(_slide-header(title, background-color.get(), logo-img.get())),
    )

    set list(marker: text(theme-color.get(), [•]))

    set enum(numbering: (it => context text(fill: theme-color.get())[*#it.*]))

    set text(size: 20pt)
    set par(justify: true)
    set align(horizon)

    v(0cm) // avoids header breaking if body is empty
    body
  }
)

//**************************************** Blank slide ****************************************\\

#let blank-slide(body) = (
  context {
    let page-num = context counter(page).display(
      "1/1",
      both: true,
    )

    set page(
      header: [
        #align(right)[
          #text(
            fill: theme-color.get(),
            weight: "semibold",
            size: 12pt,
          )[#page-num]
        ]
      ],
    )

    set list(marker: text(theme-color.get(), [•]))

    set enum(numbering: (it => context text(fill: theme-color.get())[*#it.*]))

    set text(size: 20pt)
    set par(justify: true)
    set align(horizon)
    body
  }
)

//**************************************** Bibliography ***************************************\\

#let bibliography-slide(
  bib-call,
  title: "References",
) = (
  context {
    set text(size: 19pt)
    set par(justify: true)

    set bibliography(title: text(size: 30pt)[#smallcaps(title) #v(-.85cm) #_divider(color: theme-color.get()) #v(.5cm)])

    bib-call
  }
)
