// API Response Types - Matching our standardized backend

export interface APIResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> extends APIResponse<T[]> {
  pagination?: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
}

// Common Entity Types
export interface BaseEntity {
  id?: string;
  name: string;
  description?: string;
  created_at?: string;
  updated_at?: string;
}

// Adventure Types
export interface Adventure extends BaseEntity {
  system: string;
  world_state: WorldState;
  active_session?: Session;
  players: Player[];
}

export interface Session extends BaseEntity {
  adventure_id: string;
  current_scene?: string;
  session_notes?: string;
  date_started: string;
  date_ended?: string;
  status: 'active' | 'paused' | 'completed';
}

export interface Player extends BaseEntity {
  character_name: string;
  character_class?: string;
  level?: number;
  stats?: Record<string, any>;
  inventory?: Item[];
  notes?: string;
}

export interface WorldState {
  npcs: NPC[];
  factions: Faction[];
  locations: Location[];
  story_lines: StoryLine[];
  custom_maps?: string[];
}

export interface NPC extends BaseEntity {
  role: string;
  faction?: string;
  location?: string;
  personality?: string;
  goals?: string[];
  relationships?: Record<string, string>;
}

export interface Faction extends BaseEntity {
  leader?: string;
  members: string[];
  goals: string[];
  resources?: string[];
  relationships?: Record<string, 'ally' | 'enemy' | 'neutral'>;
}

export interface Location extends BaseEntity {
  type: 'city' | 'dungeon' | 'wilderness' | 'settlement' | 'ruin' | 'other';
  parent_location?: string;
  features: string[];
  connections: string[];
  npcs: string[];
}

export interface StoryLine extends BaseEntity {
  status: 'active' | 'resolved' | 'abandoned';
  key_events: StoryEvent[];
  involved_npcs: string[];
  involved_locations: string[];
}

export interface StoryEvent extends BaseEntity {
  date: string;
  type: 'discovery' | 'conflict' | 'resolution' | 'twist' | 'other';
  description: string;
  consequences?: string[];
}

// Lookup Types
export interface Item extends BaseEntity {
  type: 'equipment' | 'valuable' | 'trade_good' | 'adventure_gear' | 'pet' | 'other';
  system: string;
  category: string;
  cost?: number;
  weight?: number;
  properties?: string[];
  rarity?: string;
  attunement?: boolean;
}

export interface Monster extends BaseEntity {
  system: string;
  type: string;
  challenge_rating?: string;
  size: 'tiny' | 'small' | 'medium' | 'large' | 'huge' | 'gargantuan';
  alignment?: string;
  stats?: Record<string, number>;
  abilities?: string[];
  actions?: string[];
  legendary_actions?: string[];
}

export interface Spell extends BaseEntity {
  system: string;
  school: string;
  level: number;
  casting_time: string;
  range: string;
  components: string[];
  duration: string;
  description: string;
  higher_levels?: string;
  ritual?: boolean;
  concentration?: boolean;
}

export interface Rule extends BaseEntity {
  system: string;
  category: string;
  content: string;
  page_reference?: string;
  tags?: string[];
}

// Oracle Types
export interface OracleTable extends BaseEntity {
  system: string;
  category: string;
  dice_range: string; // e.g., "1d6", "1d20", "1-100"
  entries: OracleEntry[];
  tags?: string[];
}

export interface OracleEntry {
  roll: string; // e.g., "1", "2-3", "4-6"
  result: string;
  sub_table?: string; // Reference to another table
}

export interface OracleResult {
  roll: number;
  result: string;
  sub_results?: OracleResult[];
}

// Generator Types
export interface GeneratorTable extends BaseEntity {
  system: string;
  category: string;
  generator_type: 'dungeon' | 'encounter' | 'treasure' | 'npc' | 'location' | 'other';
  parameters: GeneratorParameter[];
  tables: string[]; // References to oracle tables
  output_format: string;
}

export interface GeneratorParameter {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'select';
  required: boolean;
  default_value?: any;
  options?: string[]; // For select type
  description?: string;
}

export interface GeneratorResult {
  input_parameters: Record<string, any>;
  generated_content: any;
  used_tables: string[];
  metadata?: Record<string, any>;
}

// Combat Types
export interface CombatSession extends BaseEntity {
  adventure_id: string;
  participants: CombatParticipant[];
  initiative_order: string[];
  current_turn?: number;
  round: number;
  status: 'active' | 'paused' | 'completed';
  notes?: string;
}

export interface CombatParticipant extends BaseEntity {
  type: 'player' | 'npc' | 'monster';
  initiative: number;
  current_hp: number;
  max_hp: number;
  armor_class?: number;
  actions?: string[];
  conditions?: string[];
}

// Error Types
export interface APIError {
  status: number;
  message: string;
  details?: any;
}

// Request Types
export interface CreateEntityRequest<T = any> {
  data: T;
}

export interface UpdateEntityRequest<T = any> {
  data: Partial<T>;
}

export interface ListRequest {
  page?: number;
  per_page?: number;
  search?: string;
  filters?: Record<string, any>;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

// Utility Types
export type EntityType = 
  | 'adventure' | 'session' | 'player' | 'npc' | 'faction' | 'location' | 'story_line'
  | 'item' | 'monster' | 'spell' | 'rule'
  | 'oracle_table' | 'generator_table'
  | 'combat_session';

export type SystemType = 'dnd5e' | 'pathfinder2e' | 'starfinder' | 'custom';

// Response Type Guards
export function isAPIResponse(obj: any): obj is APIResponse {
  return obj && typeof obj === 'object' && 'success' in obj;
}

export function isPaginatedResponse<T>(obj: any): obj is PaginatedResponse<T> {
  return isAPIResponse(obj) && 'pagination' in obj;
} 