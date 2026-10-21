// project-home kit · frontmatter 1.0.0
//
// Reads the YAML front matter at the top of a Markdown record, such as a goal's
// GOAL.md. It understands the plain subset the records use: scalar values
// (text, quoted text, numbers, true/false, null), inline lists ([a, b]), block
// lists, and one level of nesting (a key holding a map, or a list of small maps).
//
//   import { parseFrontMatter } from './frontmatter.js'
//   const { data, body } = parseFrontMatter(markdownText)

const KEY = /^([A-Za-z0-9_][A-Za-z0-9_ .-]*?)\s*:(?:\s+(.*)|\s*)$/

export function parseFrontMatter(text) {
  const source = String(text ?? '').replace(/^﻿/, '')
  const match = source.match(/^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/)
  if (!match) return { data: {}, body: source }
  return { data: parseBlock(match[1]), body: source.slice(match[0].length) }
}

function parseBlock(yaml) {
  const lines = yaml
    .split(/\r?\n/)
    .map((raw) => ({ indent: raw.search(/\S|$/), text: raw.trim() }))
    .filter((line) => line.text !== '' && !line.text.startsWith('#'))
  const data = {}
  let i = 0
  while (i < lines.length) {
    const line = lines[i]
    const m = line.indent === 0 && line.text.match(KEY)
    if (!m) { i++; continue }
    const [, key, rest] = m
    i++
    if (rest !== undefined && rest.trim() !== '') { data[key] = scalarOrList(rest); continue }
    const children = []
    while (i < lines.length && lines[i].indent > 0) children.push(lines[i++])
    data[key] = nested(children)
  }
  return data
}

function nested(lines) {
  if (lines.length === 0) return null
  if (lines[0].text.startsWith('-')) return list(lines)
  const map = {}
  for (const line of lines) {
    const m = line.text.match(KEY)
    if (m) map[m[1]] = m[2] === undefined ? null : scalarOrList(m[2])
  }
  return map
}

function list(lines) {
  const items = []
  const base = lines[0].indent
  for (const line of lines) {
    if (line.indent === base && line.text.startsWith('-')) {
      const rest = line.text.replace(/^-\s*/, '')
      const m = rest.match(KEY)
      if (m && !/^["']/.test(rest)) items.push({ [m[1]]: m[2] === undefined ? null : scalarOrList(m[2]) })
      else items.push(rest === '' ? null : scalarOrList(rest))
    } else {
      // A further key of the map the last item started.
      const last = items[items.length - 1]
      const m = line.text.match(KEY)
      if (m && last && typeof last === 'object' && !Array.isArray(last)) {
        last[m[1]] = m[2] === undefined ? null : scalarOrList(m[2])
      }
    }
  }
  return items
}

function scalarOrList(value) {
  const v = value.trim()
  if (v.startsWith('[') && v.endsWith(']')) {
    const inner = v.slice(1, -1).trim()
    return inner === '' ? [] : splitInline(inner).map(scalar)
  }
  return scalar(v)
}

function splitInline(text) {
  const parts = []
  let current = ''
  let quote = null
  for (const ch of text) {
    if (quote) { current += ch; if (ch === quote) quote = null; continue }
    if (ch === '"' || ch === "'") { quote = ch; current += ch; continue }
    if (ch === ',') { parts.push(current); current = ''; continue }
    current += ch
  }
  parts.push(current)
  return parts.map((p) => p.trim())
}

function scalar(value) {
  const v = value.trim()
  if (v.startsWith('"') && v.endsWith('"') && v.length >= 2) {
    try { return JSON.parse(v) } catch { return v.slice(1, -1) }
  }
  if (v.startsWith("'") && v.endsWith("'") && v.length >= 2) return v.slice(1, -1).replace(/''/g, "'")
  if (v === 'true') return true
  if (v === 'false') return false
  if (v === 'null' || v === '~') return null
  if (/^-?\d+(\.\d+)?$/.test(v)) return Number(v)
  return v
}
