// project-home kit · projectdata 1.0.0
//
// Reads the project tree's shared data through the page client, by paths from
// the tree's root, so it works the same from any page, including drafts:
//
//   /goals/goals.json             the goal list
//   /goals/<slug>/GOAL.md         each goal's record, read for its front matter
//   /glossary/glossary.json       the terms
//
// A page imports it from its own folder; Dossier serves the closest kit copy:
//
//   import { loadGoals, loadGlossary, linkTo } from './_components/projectdata.js'

import { parseFrontMatter } from './frontmatter.js'

async function client() {
  const dossier = window.dossier
  if (!dossier) throw new Error('The Dossier page client is not available on this page.')
  await dossier.ready
  return dossier
}

// A relative link from the current page to a path in the tree, without the
// .html extension: linkTo('goals/') or linkTo('goals/abc/prd-interview/').
export function linkTo(treePath) {
  const page = String(window.dossier?.page?.path ?? '').replace(/^\/+/, '')
  const depth = page.split('/').length - 1
  const path = String(treePath ?? '')
    .replace(/^\/+/, '')
    .replace(/(^|\/)index\.html$/, '$1')
    .replace(/\.html$/, '')
  return ('../'.repeat(depth) || './') + path
}

async function read(path) {
  const dossier = await client()
  try {
    const doc = await dossier.read(path)
    return doc?.data ?? null
  } catch (error) {
    if (error?.code === 'forbidden') return null
    throw error
  }
}

// The goal list, each goal with its record's front matter:
// [{ slug, title, status, opened, link, path, record, pages }]
// record is the GOAL.md front matter (stage, next, waiting, …), or null when
// the record cannot be read. pages is the record's `pages` list of
// { title, path }, with each path made relative to the tree's root.
export async function loadGoals() {
  const list = await read('/goals/goals.json')
  const goals = Array.isArray(list?.goals) ? list.goals : []
  return Promise.all(
    goals.map(async (goal) => {
      const path = `goals/${goal.slug}/`
      let record = null
      try {
        const text = await read(`/${path}GOAL.md`)
        if (typeof text === 'string') record = parseFrontMatter(text).data
      } catch {
        record = null
      }
      const pages = Array.isArray(record?.pages)
        ? record.pages
            .filter((p) => p && typeof p === 'object' && p.path)
            .map((p) => ({ title: String(p.title ?? p.path), path: path + String(p.path).replace(/^\.?\//, '') }))
        : []
      return { ...goal, path, record, pages }
    }),
  )
}

// The glossary: { contexts: [], terms: [] }.
export async function loadGlossary() {
  const data = await read('/glossary/glossary.json')
  return {
    contexts: Array.isArray(data?.contexts) ? data.contexts : [],
    terms: Array.isArray(data?.terms) ? data.terms : [],
  }
}

// Read any Markdown record and return its front matter and body.
export async function loadRecord(path) {
  const text = await read(path)
  return typeof text === 'string' ? parseFrontMatter(text) : null
}
