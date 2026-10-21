// project-home kit · project-term-hints 1.1.0
//
// <project-term-hints>: underlines the first mention of each glossary term on a
// page and shows its definition in a popover on hover or tap. It never changes
// the page's own nodes: marks are CSS highlights over the text, so pages whose
// scripts keep and update their text work as before. Its look comes only from
// the theme's variables. See project-term-hints.md.

import { loadGlossary, linkTo } from './projectdata.js'

const SKIP =
  'a, button, code, pre, kbd, samp, var, h1, h2, h3, h4, h5, h6, label, input, textarea, select, option, ' +
  'script, style, svg, math, dialog, [popover], [contenteditable], [data-term-hints="off"], ' +
  'project-palette, project-term-hints, dossier-comments, dossier-copy, dossier-diff, dossier-notifications'
const HIGHLIGHT = 'project-term'
const SHOW_DELAY = 150
const HIDE_DELAY = 200
// Letters, combining marks and digits continue a word, so a term never matches
// inside a longer word, Arabic words with diacritics included.
const WORD = '\\p{L}\\p{M}\\p{N}_'

// Structure and the theme's variables only, in a layer the kit's own CSS overrides.
const STYLE = `
@layer project-kit {
  ::highlight(${HIGHLIGHT}) {
    text-decoration: underline dotted;
    text-decoration-color: var(--muted-foreground, currentColor);
  }
  html[data-project-term-hover] { cursor: help; }
  [data-part="term-popover"] {
    position: fixed;
    inset: auto;
    margin: 0;
    max-width: min(22rem, calc(100vw - 1.5rem));
    padding: 0.75rem 0.9rem;
    border: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
    border-radius: var(--radius, 0.5rem);
    background: var(--popover, Canvas);
    color: var(--popover-foreground, CanvasText);
    font: 0.9rem/1.45 var(--font-body, inherit);
    box-shadow: 0 12px 32px color-mix(in srgb, var(--foreground, CanvasText) 18%, transparent);
  }
  [data-part="term-popover"] [data-part="term-name"] { font-weight: 600; }
  [data-part="term-popover"] [data-part="term-meaning"] + [data-part="term-meaning"] {
    margin-top: 0.6rem;
    padding-top: 0.6rem;
    border-top: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
  }
  [data-part="term-popover"] [data-part="term-status"],
  [data-part="term-popover"] [data-part="term-context"],
  [data-part="term-popover"] [data-part="term-avoid"],
  [data-part="term-popover"] [data-part="term-related"] {
    color: var(--muted-foreground, inherit);
    font-size: 0.85em;
  }
  [data-part="term-popover"] [data-part="term-definition"] { margin: 0.35rem 0; }
  [data-part="term-popover"] [data-part="term-example"] { margin: 0.35rem 0; font-style: italic; }
  [data-part="term-popover"] [data-part="term-related"] a { color: var(--primary, LinkText); }
  [data-part="term-popover"] [data-part="term-proposal"] {
    margin: 0.5rem 0 0;
    padding-top: 0.5rem;
    border-top: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
  }
  [data-part="term-popover"] [data-part="term-link"] {
    display: inline-block;
    margin-top: 0.35rem;
    color: var(--primary, LinkText);
    font-size: 0.85em;
  }
}`

const escapeRegExp = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

// The text position under a point, in either form browsers offer.
function caretAt(x, y) {
  if (document.caretPositionFromPoint) {
    const p = document.caretPositionFromPoint(x, y)
    return p ? { node: p.offsetNode, offset: p.offset } : null
  }
  if (document.caretRangeFromPoint) {
    const r = document.caretRangeFromPoint(x, y)
    return r ? { node: r.startContainer, offset: r.startOffset } : null
  }
  return null
}

class ProjectTermHints extends HTMLElement {
  connectedCallback() {
    if (this.started) return
    this.started = true
    // Hints are drawn as CSS highlights; a browser without them shows none.
    if (!('highlights' in CSS)) return
    if (!document.getElementById('project-term-hints-style')) {
      const style = document.createElement('style')
      style.id = 'project-term-hints-style'
      style.textContent = STYLE
      document.head.append(style)
    }
    this.start().catch(() => {
      // Without the glossary there is nothing to mark; the page reads as before.
    })
  }

  disconnectedCallback() {
    this.observer?.disconnect()
    this.tip?.remove()
    CSS.highlights?.delete(HIGHLIGHT)
    for (const [type, handler, options] of this.listeners ?? []) document.removeEventListener(type, handler, options)
    if (this.onAway) window.removeEventListener('resize', this.onAway)
  }

  async start() {
    const { contexts, terms } = await loadGlossary()
    this.contextNames = new Map(contexts.map((c) => [c.id, c.name ?? c.id]))
    this.entries = new Map()
    for (const term of terms) {
      if (!term?.id || !term.term) continue
      const entry = this.entries.get(term.id) ?? { id: term.id }
      if (term.status === 'proposed') entry.proposal = term
      else entry.current = term
      this.entries.set(term.id, entry)
    }
    if (this.entries.size === 0) return

    // Every name a term goes by, its current name and a proposed new name. A
    // name several contexts share points at every meaning.
    this.nameToIds = new Map()
    for (const entry of this.entries.values()) {
      for (const t of [entry.current, entry.proposal]) {
        if (!t?.term) continue
        const key = t.term.toLowerCase()
        const ids = this.nameToIds.get(key) ?? []
        if (!ids.includes(entry.id)) ids.push(entry.id)
        this.nameToIds.set(key, ids)
      }
    }
    const names = [...this.nameToIds.keys()].sort((a, b) => b.length - a.length)
    this.pattern = new RegExp(`(?<![${WORD}])(${names.map(escapeRegExp).join('|')})(?:e?s)?(?![${WORD}])`, 'giu')

    this.buildPopover()
    this.root = document.querySelector(this.getAttribute('scope') || 'main') ?? document.body
    this.highlight = new Highlight()
    CSS.highlights.set(HIGHLIGHT, this.highlight)
    this.scan()
    // Highlights change no nodes, so rescanning never triggers itself.
    this.observer = new MutationObserver(() => {
      clearTimeout(this.rescan)
      this.rescan = setTimeout(() => this.scan(), 300)
    })
    this.observer.observe(this.root, { childList: true, subtree: true, characterData: true })
    this.listen()
  }

  buildPopover() {
    this.tip = document.createElement('div')
    this.tip.dataset.part = 'term-popover'
    this.tip.setAttribute('popover', 'manual')
    this.tip.addEventListener('pointerenter', () => clearTimeout(this.hideTimer))
    this.tip.addEventListener('pointerleave', () => this.scheduleHide())
    document.body.append(this.tip)
  }

  // Mark the first mention of each name inside the scope.
  scan() {
    this.marks = []
    const seen = new Set()
    const walker = document.createTreeWalker(this.root, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) =>
        node.nodeValue.trim() === '' || node.parentElement?.closest(SKIP)
          ? NodeFilter.FILTER_REJECT
          : NodeFilter.FILTER_ACCEPT,
    })
    while (walker.nextNode()) {
      const node = walker.currentNode
      this.pattern.lastIndex = 0
      let match
      while ((match = this.pattern.exec(node.nodeValue))) {
        const ids = this.nameToIds.get(match[1].toLowerCase())
        const key = ids?.join(' ')
        if (!key || seen.has(key)) continue
        seen.add(key)
        const range = new Range()
        range.setStart(node, match.index)
        range.setEnd(node, match.index + match[0].length)
        this.marks.push({ range, ids })
      }
    }
    this.highlight.clear()
    for (const mark of this.marks) this.highlight.add(mark.range)
  }

  // The mark under a point, if the point is on the marked text itself.
  markAt(x, y) {
    const caret = caretAt(x, y)
    if (!caret || caret.node?.nodeType !== Node.TEXT_NODE) return null
    for (const mark of this.marks) {
      if (!mark.range.isPointInRange(caret.node, caret.offset)) continue
      for (const rect of mark.range.getClientRects()) {
        if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) return mark
      }
    }
    return null
  }

  listen() {
    let frame = 0
    const onMove = (event) => {
      if (frame) return
      frame = requestAnimationFrame(() => {
        frame = 0
        if (this.tip.contains(event.target)) return
        const mark = this.markAt(event.clientX, event.clientY)
        document.documentElement.toggleAttribute('data-project-term-hover', Boolean(mark))
        if (mark && mark !== this.active) {
          clearTimeout(this.hideTimer)
          clearTimeout(this.showTimer)
          this.showTimer = setTimeout(() => this.show(mark), SHOW_DELAY)
        } else if (!mark && this.active) {
          this.scheduleHide()
        } else if (!mark) {
          clearTimeout(this.showTimer)
        }
      })
    }
    // A tap opens the hint at once; a tap elsewhere closes it.
    const onClick = (event) => {
      if (this.tip.contains(event.target)) return
      const mark = this.markAt(event.clientX, event.clientY)
      if (mark) this.show(mark)
      else this.hide()
    }
    const onKey = (event) => {
      if (event.key === 'Escape') this.hide()
    }
    this.onAway = () => this.hide()
    this.listeners = [
      ['pointermove', onMove, { passive: true }],
      ['click', onClick, false],
      ['keydown', onKey, false],
      ['scroll', this.onAway, { capture: true, passive: true }],
    ]
    for (const [type, handler, options] of this.listeners) document.addEventListener(type, handler, options)
    window.addEventListener('resize', this.onAway)
  }

  show(mark) {
    clearTimeout(this.showTimer)
    clearTimeout(this.hideTimer)
    const entries = mark.ids.map((id) => this.entries.get(id)).filter(Boolean)
    if (entries.length === 0) return
    this.tip.replaceChildren(...entries.map((entry) => this.render(entry, entries.length > 1)))
    this.active = mark
    if (!this.tip.matches(':popover-open')) this.tip.showPopover()
    this.place(mark)
  }

  scheduleHide() {
    clearTimeout(this.showTimer)
    clearTimeout(this.hideTimer)
    this.hideTimer = setTimeout(() => this.hide(), HIDE_DELAY)
  }

  hide() {
    clearTimeout(this.showTimer)
    clearTimeout(this.hideTimer)
    if (this.tip?.matches(':popover-open')) this.tip.hidePopover()
    this.active = null
  }

  nameOf(id) {
    const entry = this.entries.get(id)
    return (entry?.current ?? entry?.proposal)?.term ?? id
  }

  glossaryLink(id) {
    return `${linkTo('glossary/')}#${encodeURIComponent(id)}`
  }

  // One meaning of a term: its name, context, definition, example, words to
  // avoid, related terms, any proposed change, and a link to the glossary.
  render(entry, several) {
    const part = (tag, name, text) => {
      const el = document.createElement(tag)
      el.dataset.part = name
      el.textContent = text
      return el
    }
    const main = entry.current ?? entry.proposal
    const section = document.createElement('section')
    section.dataset.part = 'term-meaning'
    section.append(part('div', 'term-name', main.term))
    if (several || this.contextNames.size > 1) {
      section.append(part('div', 'term-context', this.contextNames.get(main.context) ?? main.context))
    }
    if (!entry.current) section.append(part('div', 'term-status', `Proposed by ${main.goal}`))
    section.append(part('p', 'term-definition', main.definition ?? ''))
    if (main.example) section.append(part('p', 'term-example', main.example))
    if (Array.isArray(main.avoid) && main.avoid.length) section.append(part('div', 'term-avoid', `Avoid: ${main.avoid.join(', ')}`))
    if (Array.isArray(main.related) && main.related.length) {
      const related = part('div', 'term-related', '')
      main.related.forEach((relation, i) => {
        if (i > 0) related.append(' · ')
        const link = document.createElement('a')
        link.href = this.glossaryLink(relation.to)
        link.textContent = this.nameOf(relation.to)
        related.append(`${relation.how} `, link)
      })
      section.append(related)
    }
    if (entry.current && entry.proposal) {
      const proposal = part('div', 'term-proposal', '')
      if (entry.proposal.term !== entry.current.term) proposal.append(part('div', 'term-name', entry.proposal.term))
      proposal.append(
        part('div', 'term-status', `Change proposed by ${entry.proposal.goal}`),
        part('p', 'term-definition', entry.proposal.definition ?? ''),
      )
      section.append(proposal)
    }
    const link = part('a', 'term-link', 'Open in the glossary')
    link.href = this.glossaryLink(entry.id)
    section.append(link)
    return section
  }

  place(mark) {
    const box = mark.range.getClientRects()[0] ?? mark.range.getBoundingClientRect()
    const pop = this.tip.getBoundingClientRect()
    const gap = 8
    let top = box.bottom + gap
    if (top + pop.height > window.innerHeight - gap) top = Math.max(gap, box.top - gap - pop.height)
    const left = Math.max(gap, Math.min(box.left, window.innerWidth - pop.width - gap))
    this.tip.style.top = `${top}px`
    this.tip.style.left = `${left}px`
  }
}

if (!customElements.get('project-term-hints')) customElements.define('project-term-hints', ProjectTermHints)
