#let _theme-colors = (
  bluey: rgb("5fd3bc"),
  darkbluey: rgb("51B4C5"),
  reddy: rgb("EB576A"),
  greeny: rgb("4CCC61"),
  dusty: rgb("EAE3D0"),
  yelly: rgb("C4853D"),
  purply: rgb("862A70"),
  darky: rgb("505050"),
  darker: rgb("333333"),
)

//************************************************************************\\

#let _resize-text(body) = layout(size => {
  let font-size = text.size
  let (height,) = measure(
    block(width: size.width, text(size: font-size)[#body]),
  )

  let max_height = size.height

  while height > max_height {
    font-size -= 0.2pt
    height = measure(
      block(width: size.width, text(size: font-size)[#body]),
    ).height
  }

  block(
    height: height,
    width: 100%,
    text(size: font-size)[#body],
  )
})

//************************************************************************\\

#let _divider(color: none) = {
  line(
    length: 100%,
    stroke: 2.5pt + color,
  )
}

//************************************************************************\\

#let _slide-header(title, color, logo) = {
  rect(
    fill: color,
    width: 100%,
    height: 1.6cm,
    inset: .6cm,
    text(white, weight: "semibold", size: 24pt)[
      #grid(
      columns: (1fr, 60pt, 90pt),
      gutter: 3pt,
      title,
      scale(15%, logo),
      )
  ],
  )
}

//************************************************************************\\

#let _make-frontpage(
  title,
  subtitle,
  authors,
  info,
  theme-color,
  background-color,
  logo,
  logo-alt,
) = {

  set align(left + horizon)
  set page(footer: none)
  set page(fill: background-color)

  v(-.95cm)

  let behind(..args) = {
    v(-1.95cm)
    h(-2.95cm)
    box(place(..args))
    sym.wj
    h(0pt, weak: true)
  }

  grid(
    columns: (6fr, 1fr),
    gutter: 30pt,
    logo,
    behind(logo-alt),
  )

  v(0.95cm)

  text(36pt, weight: "bold", fill: white)[#smallcaps(title)]

  v(-.95cm)

  if subtitle != none {
    set text(24pt, fill: white)
    v(.1cm)
    subtitle
  }

  let subtext = []

  if authors != none {
    subtext += text(22pt, weight: "regular", fill: white)[#authors]
  }

  if info != none {
    subtext += text(20pt, fill: theme-color, weight: "regular")[#v(-.15cm) #info]
  }

  _divider(color: theme-color)
  [#subtext]

}
