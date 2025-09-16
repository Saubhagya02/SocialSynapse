// frontend/src/types/index.ts
export interface User {
  id: string;
  email: string;
  name: string;
  title?: string;
  industry?: string;
  skills?: string[];
  target_audience?: string;
  brand_voice?: string;
  linkedin_connected: boolean;
  created_at: string;
}

export interface Post {
  id: string;
  content: string;
  content_type: ContentType;
  hashtags: string[];
  media_urls?: string[];
  status: PostStatus;
  scheduled_time?: string;
  published_at?: string;
  engagement_rate: number;
  virality_score: number;
  likes: number;
  comments: number;
  shares: number;
  views: number;
  created_at: string;
}

export type ContentType = 'text_post' | 'article' | 'carousel' | 'poll' | 'video';
export type PostStatus = 'draft' | 'scheduled' | 'published' | 'failed';

export interface GeneratedContent {
  id: string;
  content: string;
  hashtags: string[];
  content_type: string;
  tone: string;
  estimated_engagement: number;
  best_posting_time: string;
  variations?: string[];
}

export interface Analytics {
  totalPosts: number;
  totalEngagement: number;
  profileViews: number;
  avgEngagementRate: number;
  connectionGrowth: number;
  viralPosts: number;
  scheduledPosts: number;
}

export interface TrendingTopic {
  topic: string;
  relevance_score: number;
  suggested_angles: string[];
  best_content_type: string;
}