// project-home kit · project-palette 1.1.0
//
// <project-palette>: a command palette for the project tree. It owns behaviour
// and accessibility, and takes its look only from the theme's variables, so a
// new brand restyles it through _theme.css. See project-palette.md.

import { rank, highlight } from './fuzzy.js'
import { loadGoals, loadGlossary, linkTo } from './projectdata.js'

const GLOSSARY_PREFIX = /^gs\s/
const LIMIT = 50
let count = 0

// What behaviour needs (hidden parts stay hidden, the status is read aloud
// without being seen), then a look built only from the theme's variables, in a
// layer the kit's own CSS overrides.
const BASE_CSS = `
project-palette [hidden] { display: none !important; }
project-palette [data-part="status"] {
  position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
  overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0;
}
@layer project-kit {
  project-palette [data-part="trigger"] {
    display: inline-flex; align-items: center; gap: 0.5em;
    padding: 0.3em 0.6em;
    border: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
    border-radius: var(--radius, 0.5rem);
    background: var(--background, Canvas);
    color: var(--muted-foreground, CanvasText);
    font: inherit; font-family: var(--font-body, inherit);
    cursor: pointer;
  }
  project-palette [data-part="trigger"] kbd {
    font-family: var(--font-mono, monospace); font-size: 0.8em;
    padding: 0.05em 0.35em;
    border: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
    border-radius: calc(var(--radius, 0.5rem) - 2px);
  }
  project-palette [data-part="dialog"] {
    width: min(40rem, calc(100vw - 2rem));
    margin: 12vh auto auto;
    padding: 0;
    border: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
    border-radius: calc(var(--radius, 0.5rem) + 4px);
    background: var(--popover, Canvas);
    color: var(--popover-foreground, CanvasText);
    font-family: var(--font-body, inherit);
    box-shadow: 0 24px 60px color-mix(in srgb, var(--foreground, CanvasText) 22%, transparent);
  }
  project-palette [data-part="dialog"]::backdrop { background: color-mix(in srgb, var(--foreground, CanvasText) 35%, transparent); }
  project-palette [data-part="field"] {
    display: flex; align-items: center; gap: 0.5rem;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border, color-mix(in srgb, CanvasText 18%, transparent));
  }
  project-palette [data-part="chip"] {
    padding: 0.1rem 0.5rem;
    border-radius: calc(var(--radius, 0.5rem) - 2px);
    background: var(--accent, color-mix(in srgb, CanvasText 10%, transparent));
    color: var(--accent-foreground, inherit);
    font-size: 0.8em; white-space: nowrap;
  }
  project-palette [data-part="input"] {
    flex: 1; min-width: 0;
    border: 0; outline: 0; background: transparent; color: inherit;
    font: inherit; font-size: 1rem;
  }
  project-palette [data-part="list"] {
    list-style: none; margin: 0; padding: 0.4rem;
    max-height: min(55vh, 26rem); overflow: auto;
  }
  project-palette [data-part="item"] {
    display: grid; gap: 0.1rem;
    padding: 0.5rem 0.75rem;
    border-radius: calc(var(--radius, 0.5rem) - 2px);
    cursor: pointer;
  }
  project-palette [data-part="item"][data-active] {
    background: var(--accent, color-mix(in srgb, CanvasText 10%, transparent));
    color: var(--accent-foreground, inherit);
  }
  project-palette [data-part="detail"],
  project-palette [data-part="badge"] {
    color: var(--muted-foreground, inherit); font-size: 0.85em;
  }
  project-palette [data-part="item"][data-active] [data-part="detail"] { color: inherit; opacity: 0.8; }
  project-palette mark { background: transparent; color: var(--primary, inherit); font-weight: 600; }
  project-palette [data-part="empty"] {
    margin: 0; padding: 1rem; text-align: center;
    color: var(--muted-foreground, inherit);
  }
  project-palette :focus-visible { outline: 2px solid var(--ring, Highlight); outline-offset: 2px; }
  project-palette [data-part="input"]:focus-visible { outline: 0; }
}`

class ProjectPalette extends HTMLElement {
  connectedCallback() {
    if (this.dialog) return
    if (!document.getElementById('project-palette-base')) {
      const style = document.createElement('style')
      style.id = 'project-palette-base'
      style.textContent = BASE_CSS
      document.head.append(style)
    }
    const id = `project-palette-${++count}`
    this.mode = 'pages'
    this.items = { pages: [], glossary: [] }
    this.results = []
    this.active = -1

    this.trigger = this.querySelector('[data-part="trigger"]')
    if (!this.trigger) {
      this.trigger = document.createElement('button')
      this.trigger.type = 'button'
      this.trigger.dataset.part = 'trigger'
      const kbd = document.createElement('kbd')
      kbd.textContent = /Mac|iPhone|iPad/.test(navigator.userAgent) ? '⌘K' : 'Ctrl K'
      this.trigger.append(this.getAttribute('label') ?? 'Search', ' ', kbd)
      this.append(this.trigger)
    }
    this.trigger.setAttribute('aria-haspopup', 'dialog')
    this.trigger.setAttribute('aria-keyshortcuts', 'Meta+K Control+K')

    this.dialog = document.createElement('dialog')
    this.dialog.dataset.part = 'dialog'
    this.dialog.setAttribute('aria-label', this.getAttribute('dialog-label') ?? 'Search the project')
    this.dialog.innerHTML = `
      <div data-part="field">
        <span data-part="chip" hidden>Glossary</span>
        <input data-part="input" type="text" role="combobox" autocomplete="off" spellcheck="false"
          aria-autocomplete="list" aria-expanded="true" aria-controls="${id}-list">
      </div>
      <ul data-part="list" role="listbox" id="${id}-list" aria-label="Results"></ul>
      <p data-part="empty" hidden></p>`
    this.append(this.dialog)
    this.status = document.createElement('div')
    this.status.dataset.part = 'status'
    this.status.setAttribute('role', 'status')
    this.status.setAttribute('aria-live', 'polite')
    this.append(this.status)

    this.chip = this.dialog.querySelector('[data-part="chip"]')
    this.input = this.dialog.querySelector('[data-part="input"]')
    this.list = this.dialog.querySelector('[data-part="list"]')
    this.empty = this.dialog.querySelector('[data-part="empty"]')
    this.idBase = id

    this.trigger.addEventListener('click', () => this.open())
    this.input.addEventListener('input', () => this.onInput())
    this.input.addEventListener('keydown', (event) => this.onKeydown(event))
    this.list.addEventListener('click', (event) => {
      const option = event.target.closest('[role="option"]')
      if (option) this.activate(Number(option.dataset.index), event)
    })
    this.list.addEventListener('mousemove', (event) => {
      const option = event.target.closest('[role="option"]')
      if (option && Number(option.dataset.index) !== this.active) this.setActive(Number(option.dataset.index))
    })
    this.dialog.addEventListener('close', () => this.onClose())
    this.dialog.addEventListener('click', (event) => {
      if (event.target === this.dialog) this.dialog.close()
    })
    this.onShortcut = (event) => {
      if (event.key?.toLowerCase() !== 'k' || !(event.metaKey || event.ctrlKey) || event.altKey) return
      if (document.documentElement.hasAttribute('data-dossier-embedded')) return
      event.preventDefault()
      if (this.dialog.open) this.dialog.close()
      else this.open()
    }
    document.addEventListener('keydown', this.onShortcut)
    this.setMode('pages')
  }

  disconnectedCallback() {
    document.removeEventListener('keydown', this.onShortcut)
  }

  async open() {
    if (this.dialog.open) return
    this.returnFocus = document.activeElement
    this.input.value = ''
    this.setMode('pages')
    this.dialog.showModal()
    this.input.focus()
    this.render()
    await this.load()
    this.render()
  }

  async load() {
    this.dataset.state = 'loading'
    try {
      const [goals, glossary] = await Promise.all([loadGoals(), loadGlossary()])
      const pages = [
        { kind: 'page', title: 'Home', detail: 'Project home', path: '' },
        { kind: 'page', title: 'Goals', detail: 'Every goal and where it stands', path: 'goals/' },
        { kind: 'page', title: 'Glossary', detail: 'Project vocabulary', path: 'glossary/' },
      ]
      for (const goal of goals) {
        const stage = goal.record?.stage ? String(goal.record.stage) : ''
        const detail = goal.status === 'done' ? 'Done' : stage
        pages.push({ kind: 'goal', title: String(goal.title ?? goal.slug), detail, path: goal.path, status: goal.status })
        for (const page of goal.pages) {
          pages.push({ kind: 'goal-page', title: page.title, detail: String(goal.title ?? goal.slug), path: page.path })
        }
      }
      const contextNames = new Map(glossary.contexts.map((c) => [c.id, c.name ?? c.id]))
      const terms = glossary.terms.map((term) => ({
        kind: 'term',
        title: String(term.term ?? ''),
        detail: String(term.definition ?? ''),
        avoid: Array.isArray(term.avoid) ? term.avoid.join(', ') : String(term.avoid ?? ''),
        // Name the context when there are several, so one word's meanings stay apart.
        context: contextNames.size > 1 ? (contextNames.get(term.context) ?? term.context ?? '') : '',
        status: term.status ?? 'current',
        goal: term.goal ?? '',
      }))
      this.items = { pages, glossary: terms }
      this.dataset.state = 'ready'
    } catch (error) {
      this.dataset.state = 'error'
      this.error = error
    }
  }

  setMode(mode) {
    this.mode = mode
    this.dataset.mode = mode
    this.chip.hidden = mode !== 'glossary'
    this.input.placeholder =
      mode === 'glossary'
        ? this.getAttribute('glossary-placeholder') ?? 'Search the glossary; Enter copies the term'
        : this.getAttribute('placeholder') ?? 'Search pages and goals; type “gs ” for the glossary'
    this.input.setAttribute('aria-label', mode === 'glossary' ? 'Search the glossary' : 'Search pages and goals')
  }

  onInput() {
    if (this.mode === 'pages' && GLOSSARY_PREFIX.test(this.input.value)) {
      this.input.value = this.input.value.replace(GLOSSARY_PREFIX, '')
      this.setMode('glossary')
    }
    this.render()
  }

  onKeydown(event) {
    const last = this.results.length - 1
    if (event.key === 'ArrowDown') { event.preventDefault(); this.setActive(this.active >= last ? 0 : this.active + 1) }
    else if (event.key === 'ArrowUp') { event.preventDefault(); this.setActive(this.active <= 0 ? last : this.active - 1) }
    else if (event.key === 'Home' && event.ctrlKey) { event.preventDefault(); this.setActive(0) }
    else if (event.key === 'End' && event.ctrlKey) { event.preventDefault(); this.setActive(last) }
    else if (event.key === 'Enter') { event.preventDefault(); if (this.active >= 0) this.activate(this.active, event) }
    else if (event.key === 'Backspace' && this.mode === 'glossary' && this.input.value === '' ) {
      event.preventDefault()
      this.setMode('pages')
      this.render()
    }
  }

  render() {
    const query = this.input.value
    const glossary = this.mode === 'glossary'
    const items = glossary ? this.items.glossary : this.items.pages
    const fields = glossary
      ? [
          { name: 'title', weight: 3, get: (i) => i.title },
          { name: 'avoid', weight: 2, get: (i) => i.avoid },
          { name: 'detail', weight: 1, get: (i) => i.detail },
        ]
      : [
          { name: 'title', weight: 2, get: (i) => i.title },
          { name: 'detail', weight: 1, get: (i) => i.detail },
        ]
    this.results = rank(query, items, fields).slice(0, LIMIT)
    this.list.replaceChildren(
      ...this.results.map((result, index) => {
        const { item, ranges } = result
        const option = document.createElement('li')
        option.id = `${this.idBase}-option-${index}`
        option.setAttribute('role', 'option')
        option.setAttribute('aria-selected', 'false')
        option.dataset.part = 'item'
        option.dataset.index = String(index)
        option.dataset.kind = item.kind
        if (item.status) option.dataset.status = item.status
        const title = document.createElement('span')
        title.dataset.part = 'title'
        title.append(highlight(item.title, ranges.title))
        option.append(title)
        if (item.detail) {
          const detail = document.createElement('span')
          detail.dataset.part = 'detail'
          detail.append(highlight(item.detail, ranges.detail))
          option.append(detail)
        }
        const notes = glossary
          ? [item.context, item.status === 'proposed' ? (item.goal ? `Proposed · ${item.goal}` : 'Proposed') : ''].filter(Boolean)
          : []
        if (notes.length) {
          const badge = document.createElement('span')
          badge.dataset.part = 'badge'
          badge.textContent = notes.join(' · ')
          option.append(badge)
        }
        return option
      }),
    )
    const state = this.dataset.state
    this.empty.hidden = this.results.length > 0
    this.empty.textContent =
      state === 'error' ? 'Could not load the project’s pages.'
      : state === 'loading' && items.length === 0 ? 'Loading…'
      : glossary ? 'No matching terms.' : 'No matching pages.'
    this.setActive(this.results.length ? 0 : -1)
    clearTimeout(this.announceTimer)
    this.announceTimer = setTimeout(() => {
      const n = this.results.length
      this.announce(n === 0 ? this.empty.textContent : `${n} ${n === 1 ? 'result' : 'results'}`)
    }, 300)
  }

  setActive(index) {
    const previous = this.list.querySelector('[aria-selected="true"]')
    if (previous) { previous.setAttribute('aria-selected', 'false'); delete previous.dataset.active }
    this.active = index
    const option = index >= 0 ? this.list.children[index] : null
    if (option) {
      option.setAttribute('aria-selected', 'true')
      option.dataset.active = ''
      this.input.setAttribute('aria-activedescendant', option.id)
      option.scrollIntoView({ block: 'nearest' })
    } else {
      this.input.removeAttribute('aria-activedescendant')
    }
  }

  async activate(index, event) {
    const result = this.results[index]
    if (!result) return
    const { item } = result
    if (item.kind === 'term') {
      const copied = await copy(item.title, this.dialog)
      this.dialog.close()
      this.announce(copied ? `Copied “${item.title}”` : `Could not copy “${item.title}”`)
      this.dispatchEvent(new CustomEvent('project-palette:copy', { detail: { term: item.title, copied }, bubbles: true }))
      return
    }
    const href = linkTo(item.path)
    this.dialog.close()
    if (event?.metaKey || event?.ctrlKey) window.open(href, '_blank', 'noopener')
    else window.location.href = href
  }

  onClose() {
    this.setActive(-1)
    if (this.returnFocus && typeof this.returnFocus.focus === 'function') this.returnFocus.focus()
  }

  announce(text) {
    this.status.textContent = ''
    requestAnimationFrame(() => { this.status.textContent = text })
  }
}

// The fallback textarea goes inside the open dialog: a modal dialog makes the
// rest of the page inert, so a textarea elsewhere cannot be selected.
async function copy(text, container) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    const area = document.createElement('textarea')
    area.value = text
    area.setAttribute('readonly', '')
    area.style.position = 'fixed'
    area.style.opacity = '0'
    container.append(area)
    area.select()
    let ok = false
    try { ok = document.execCommand('copy') } catch { ok = false }
    area.remove()
    return ok
  }
}

if (!customElements.get('project-palette')) customElements.define('project-palette', ProjectPalette)
