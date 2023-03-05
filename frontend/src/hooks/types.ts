import { ComputedRef } from 'vue'

export type Message = {
    message: string;
    sender: 'user' | 'bot';
    created_at: string;
};

export type User = {
    sub: string;
    nickname?: string;
    name?: string;
    picture?: string;
    updated_at?: string;
    email?: string;
    email_verified?: boolean;
};

export type Notify = {
    message: string;
    status:string;
}