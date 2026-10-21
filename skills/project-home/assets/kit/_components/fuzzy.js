// project-home kit · fuzzy 1.0.0
//
// Fuzzy matching for the command palette and any page that searches the
// project, such as the glossary page. Every word of the query must match a
// field, as a substring or as letters in order; substrings, word starts and
// consecutive letters rank higher.
//
//   import { rank, highlight } from './fuzzy.js'
//   const results = rank('drft rev', items, [
//     { name: 'title', weight: 2, get: (item) => item.title },
//     { name: 'detail', weight: 1, get: (item) => item.detail },
//   ])
//   // → [{ item, score, ranges: { title: [[start, end], …], detail: […] } }]
//   element.append(highlight(text, result.ranges.title))

const isBoundary = (text, i) => i === 0 || /[\s\-_/.·:([]/.test(text[i - 1])

// Score one query word against one text: { score, ranges } or null.
export function matchWord(word, text) {
  const q = word.toLowerCase()
  const t = String(text ?? '').toLowerCase()
  if (q === '' || t === '') return null
  const at = t.indexOf(q)
  if (at >= 0) {
    // Prefer an occurrence at a word start.
    let best = at
    for (let i = at; i >= 0 && i < t.length; i = t.indexOf(q, i + 1)) {
      if (isBoundary(t, i)) { best = i; break }
    }
    const score = 100 + (best === 0 ? 30 : 0) + (isBoundary(t, best) ? 20 : 0) + q.length * 2 - best * 0.05
    return { score, ranges: [[best, best + q.length]] }
  }
  // Letters in order, preferring word starts.
  const ranges = []
  let score = 0
  let from = 0
  let previous = -2
  for (const ch of q) {
    let i = t.indexOf(ch, from)
    if (i < 0) return null
    for (let j = i; j >= 0; j = t.indexOf(ch, j + 1)) {
      if (isBoundary(t, j) && j - i < 12) { i = j; break }
      if (j - i >= 12) break
    }
    score += 4 + (i === previous + 1 ? 8 : 0) + (isBoundary(t, i) ? 6 : 0) - Math.min(i - from, 10) * 0.3
    if (ranges.length && ranges[ranges.length - 1][1] === i) ranges[ranges.length - 1][1] = i + 1
    else ranges.push([i, i + 1])
    previous = i
    from = i + 1
  }
  return { score: Math.min(score, 90), ranges }
}

// Rank items by a query across weighted fields. An empty query keeps every
// item in its original order.
export function rank(query, items, fields) {
  const words = String(query ?? '').trim().split(/\s+/).filter(Boolean)
  if (words.length === 0) return items.map((item) => ({ item, score: 0, ranges: {} }))
  const results = []
  for (const item of items) {
    let total = 0
    const ranges = {}
    let matchedAll = true
    for (const word of words) {
      let best = null
      for (const field of fields) {
        const m = matchWord(word, field.get(item))
        if (m && (!best || m.score * (field.weight ?? 1) > best.score)) {
          best = { score: m.score * (field.weight ?? 1), field: field.name, ranges: m.ranges }
        }
      }
      if (!best) { matchedAll = false; break }
      total += best.score
      ;(ranges[best.field] ??= []).push(...best.ranges)
    }
    if (matchedAll) {
      for (const name in ranges) ranges[name] = merge(ranges[name])
      results.push({ item, score: total, ranges })
    }
  }
  return results.sort((a, b) => b.score - a.score)
}

function merge(ranges) {
  const sorted = [...ranges].sort((a, b) => a[0] - b[0])
  const out = []
  for (const r of sorted) {
    const last = out[out.length - 1]
    if (last && r[0] <= last[1]) last[1] = Math.max(last[1], r[1])
    else out.push([...r])
  }
  return out
}

// The text as a fragment with each matched range in a <mark>.
export function highlight(text, ranges = []) {
  const value = String(text ?? '')
  const fragment = document.createDocumentFragment()
  let at = 0
  for (const [start, end] of merge(ranges)) {
    if (start > at) fragment.append(value.slice(at, start))
    const mark = document.createElement('mark')
    mark.textContent = value.slice(start, end)
    fragment.append(mark)
    at = end
  }
  if (at < value.length) fragment.append(value.slice(at))
  return fragment
}
