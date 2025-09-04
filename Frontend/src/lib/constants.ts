// frontend/src/lib/constants.ts
export const CONTENT_TYPES = [
  { value: 'text_post', label: 'Text Post', icon: 'FileText' },
  { value: 'article', label: 'Article', icon: 'FileText' },
  { value: 'carousel', label: 'Carousel', icon: 'Image' },
  { value: 'poll', label: 'Poll', icon: 'BarChart' },
  { value: 'video', label: 'Video Script', icon: 'Video' },
];

export const TONE_OPTIONS = [
  { value: 'professional', label: 'Professional' },
  { value: 'casual', label: 'Casual' },
  { value: 'inspirational', label: 'Inspirational' },
  { value: 'educational', label: 'Educational' },
  { value: 'humorous', label: 'Humorous' },
  { value: 'thought_provoking', label: 'Thought-provoking' },
];

export const POSTING_TIMES = {
  morning: { label: 'Morning (8-10 AM)', hours: [8, 9, 10] },
  lunch: { label: 'Lunch (12-1 PM)', hours: [12, 13] },
  evening: { label: 'Evening (5-7 PM)', hours: [17, 18, 19] },
};

export const INDUSTRIES = [
  'Technology',
  'Finance',
  'Healthcare',
  'Marketing',
  'Sales',
  'Education',
  'Consulting',
  'Real Estate',
  'Manufacturing',
  'Retail',
  'Other',
];