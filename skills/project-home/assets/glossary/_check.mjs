#!/usr/bin/env node
// project-home kit · glossary check 1.1.0
//
// Checks the project glossary before it is published:
//
//   node glossary/_check.mjs [path to glossary.json]
//
// It reads glossary/glossary.json beside this file unless given a path,
// prints every problem with where it is, and exits 1 when there is any.

import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const path = process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), 'glossary.json')
const problems = []
const problem = (where, message) => problems.push(`${where}: ${message}`)

const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/
const DATE = /^\d{4}-\d{2}-\d{2}$/
const isText = (v) => typeof v === 'string' && v.trim() !== ''
const isTextList = (v) => Array.isArray(v) && v.every(isText)

let raw
try {
  raw = readFileSync(path, 'utf8')
} catch (error) {
  console.error(`Cannot read ${path}: ${error.message}`)
  process.exit(1)
}

if (/^(<{7}|={7}|>{7})( |$)/m.test(raw)) {
  console.error(`${path} still holds merge conflict markers. Resolve them, then run the check again.`)
  process.exit(1)
}

let glossary
try {
  glossary = JSON.parse(raw)
} catch (error) {
  console.error(`${path} is not valid JSON: ${error.message}`)
  process.exit(1)
}

const only = (where, value, allowed) => {
  for (const key of Object.keys(value)) {
    if (!allowed.includes(key)) problem(where, `unknown field "${key}"; allowed: ${allowed.join(', ')}`)
  }
}

if (typeof glossary !== 'object' || glossary === null || Array.isArray(glossary)) {
  problem('glossary', 'must be an object with "version", "contexts" and "terms"')
} else {
  only('glossary', glossary, ['version', 'contexts', 'terms'])
  if (glossary.version !== 1) problem('glossary.version', 'must be 1')
  if (!Array.isArray(glossary.contexts) || glossary.contexts.length === 0) {
    problem('glossary.contexts', 'must be a list with at least one context')
  }
  if (!Array.isArray(glossary.terms)) problem('glossary.terms', 'must be a list')
}

const contexts = new Set()
for (const [i, context] of (Array.isArray(glossary?.contexts) ? glossary.contexts : []).entries()) {
  const where = `contexts[${i}]`
  if (typeof context !== 'object' || context === null || Array.isArray(context)) {
    problem(where, 'must be an object')
    continue
  }
  only(where, context, ['id', 'name', 'about'])
  if (!isText(context.id) || !SLUG.test(context.id)) problem(`${where}.id`, 'must be lowercase letters, digits and hyphens')
  else if (contexts.has(context.id)) problem(`${where}.id`, `"${context.id}" is used by another context`)
  else contexts.add(context.id)
  if (!isText(context.name)) problem(`${where}.name`, 'must be text')
  if (context.about !== undefined && typeof context.about !== 'string') problem(`${where}.about`, 'must be text')
}

const current = new Map() // id → entry
const proposed = new Map() // id → entry
const names = new Map() // context + name → id
for (const [i, term] of (Array.isArray(glossary?.terms) ? glossary.terms : []).entries()) {
  const label = typeof term?.term === 'string' ? ` ("${term.term}")` : ''
  const where = `terms[${i}]${label}`
  if (typeof term !== 'object' || term === null || Array.isArray(term)) {
    problem(where, 'must be an object')
    continue
  }
  only(where, term, ['id', 'term', 'definition', 'example', 'avoid', 'related', 'context', 'status', 'goal', 'since'])
  for (const field of ['term', 'definition']) {
    if (!isText(term[field])) problem(`${where}.${field}`, 'must be text')
  }
  if (term.example !== undefined && !isText(term.example)) problem(`${where}.example`, 'must be one sentence of text')
  if (term.avoid !== undefined && !Array.isArray(term.avoid)) problem(`${where}.avoid`, 'must be a list of words')
  else if (Array.isArray(term.avoid) && !isTextList(term.avoid)) problem(`${where}.avoid`, 'must hold only text')
  if (!contexts.has(term.context)) problem(`${where}.context`, `"${term.context}" is not a context in "contexts"`)
  if (term.since !== undefined && !(isText(term.since) && DATE.test(term.since))) {
    problem(`${where}.since`, 'must be a date as YYYY-MM-DD')
  }

  const [prefix, slug, ...rest] = typeof term.id === 'string' ? term.id.split('.') : []
  if (!SLUG.test(prefix ?? '') || !SLUG.test(slug ?? '') || rest.length > 0) {
    problem(`${where}.id`, 'must be "<context id>.<slug>", lowercase letters, digits and hyphens')
  } else if (prefix !== term.context) {
    problem(`${where}.id`, `must start with its context, "${term.context}."`)
  }

  if (term.status === 'current') {
    if (term.goal !== undefined) problem(`${where}.goal`, 'a current term names no goal')
    if (current.has(term.id)) problem(`${where}.id`, `"${term.id}" already has a current entry`)
    else current.set(term.id, term)
  } else if (term.status === 'proposed') {
    if (!isText(term.goal) || !SLUG.test(term.goal)) problem(`${where}.goal`, "a proposed term names its goal's slug")
    if (proposed.has(term.id)) {
      const other = proposed.get(term.id)
      problem(`${where}.id`, `"${term.id}" is already proposed by goal "${other.goal}"; one proposal per term at a time, so the goals' owners need to agree first`)
    } else proposed.set(term.id, term)
  } else {
    problem(`${where}.status`, 'must be "current" or "proposed"')
  }

  if (isText(term.term) && contexts.has(term.context) && typeof term.id === 'string') {
    const key = `${term.context}\u0000${term.term.trim().toLowerCase()}`
    const owner = names.get(key)
    if (owner !== undefined && owner !== term.id) {
      problem(`${where}.term`, `"${term.term}" is already the name of "${owner}" in context "${term.context}"; one name per concept`)
    } else names.set(key, term.id)
  }
}

// Checks that need every entry: relations point at real terms, and a proposal
// that renames a term keeps the old name among the words to avoid.
const ids = new Set([...current.keys(), ...proposed.keys()])
for (const [i, term] of (Array.isArray(glossary?.terms) ? glossary.terms : []).entries()) {
  if (typeof term !== 'object' || term === null || Array.isArray(term)) continue
  const where = `terms[${i}]${typeof term.term === 'string' ? ` ("${term.term}")` : ''}`
  if (term.related !== undefined) {
    if (!Array.isArray(term.related)) problem(`${where}.related`, 'must be a list of { "to", "how" }')
    else {
      for (const [j, relation] of term.related.entries()) {
        const at = `${where}.related[${j}]`
        if (typeof relation !== 'object' || relation === null || Array.isArray(relation)) {
          problem(at, 'must be { "to": "<term id>", "how": "<short verb phrase>" }')
          continue
        }
        only(at, relation, ['to', 'how'])
        if (!isText(relation.how)) problem(`${at}.how`, 'must be a short verb phrase, such as "has many"')
        if (!isText(relation.to)) problem(`${at}.to`, 'must be a term id')
        else if (relation.to === term.id) problem(`${at}.to`, 'a term does not relate to itself')
        else if (!ids.has(relation.to)) problem(`${at}.to`, `"${relation.to}" is not a term in the glossary`)
      }
    }
  }
  if (term.status === 'proposed' && current.has(term.id) && isText(term.term)) {
    const before = current.get(term.id).term
    const renamed = isText(before) && before.trim().toLowerCase() !== term.term.trim().toLowerCase()
    const kept = Array.isArray(term.avoid) && term.avoid.some((w) => isText(w) && w.trim().toLowerCase() === before.trim().toLowerCase())
    if (renamed && !kept) problem(`${where}.avoid`, `renames "${before}", so "${before}" belongs among the words to avoid`)
  }
}

if (problems.length > 0) {
  console.error(`${path}: ${problems.length} problem${problems.length === 1 ? '' : 's'}`)
  for (const line of problems) console.error(`- ${line}`)
  process.exit(1)
}
const count = (Array.isArray(glossary.terms) ? glossary.terms : []).length
console.log(`${path}: valid (${contexts.size} context${contexts.size === 1 ? '' : 's'}, ${count} entr${count === 1 ? 'y' : 'ies'}).`)
