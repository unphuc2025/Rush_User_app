import apiClient from './apiClient';

export interface Venue {
    id: string;
    court_name: string;
    location: string;
    game_type: string;
    prices: string;
    description?: string;
    photos?: string[]; // Array of photo URLs
    videos?: string[]; // Array of video URLs
    created_at?: string;
    updated_at?: string;
}

export interface VenuesFilter {
    location?: string;
    game_type?: string | string[];
    price_min?: number;
    price_max?: number;
    amenities?: string[];
    city?: string;
}

export const venuesApi = {
    /**
     * Fetch venues filtered by location and game type
     */
    getVenues: async (filter?: VenuesFilter) => {
        try {
            console.log('[COURTS API] Fetching courts with filter:', filter);

            const params: Record<string, string> = {};
            if (filter?.city) params.city = filter.city;
            if (filter?.location) params.location = filter.location;
            if (filter?.game_type) {
                params.game_type = Array.isArray(filter.game_type)
                    ? filter.game_type.join(',')
                    : filter.game_type;
            }

            // Construct query string
            const queryString = new URLSearchParams(params).toString();
            const endpoint = `/courts/${queryString ? `?${queryString}` : ''}`;

            const data = await apiClient.get<Venue[]>(endpoint);

            console.log('[COURTS API] Fetched courts:', data?.length || 0);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            console.error('[COURTS API] Exception:', error);
            return {
                success: false,
                data: [],
                error: error.message,
            };
        }
    },

    /**
     * Get a single venue by ID
     */
    getVenueById: async (venueId: string) => {
        try {
            const data = await apiClient.get<Venue>(`/venues/${venueId}`);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            return {
                success: false,
                data: null,
                error: error.message,
            };
        }
    },

    /**
     * Get available slots for a court on a specific date
     */
    getAvailableSlots: async (courtId: string, date: string) => {
        try {
            console.log('[COURTS API] Fetching available slots for court:', courtId, 'date:', date);
            const data = await apiClient.get<{
                court_id: string;
                date: string;
                slots: Array<{
                    time: string;
                    display_time: string;
                    price: number;
                    available: boolean;
                }>;
            }>(`/courts/${courtId}/available-slots?date=${date}`);

            console.log('[COURTS API] Available slots:', data.slots?.length || 0);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            console.error('[COURTS API] Error fetching slots:', error);
            return {
                success: false,
                data: null,
                error: error.message,
            };
        }
    },

    /**
     * Seed venues (dev only)
     */
    seedVenues: async () => {
        try {
            const data = await apiClient.post<Venue[]>('/venues/seed', {});
            return { success: true, data };
        } catch (error: any) {
            return { success: false, error: error.message };
        }
    }
};

export interface CouponValidationResult {
    valid: boolean;
    discount_percentage?: number;
    discount_amount?: number;
    final_amount?: number;
    message: string;
}

export interface AvailableCoupon {
    code: string;
    discount_type: string;
    discount_value: number;
    min_order_value?: number;
    description?: string;
}

// Coupons API
export const couponsApi = {
    /**
     * Get all available active coupons for dropdown
     */
    getAvailableCoupons: async () => {
        try {
            console.log('[COUPONS API] Fetching available coupons');

            const data = await apiClient.get<AvailableCoupon[]>('/coupons/available');

            console.log('[COUPONS API] Available coupons:', data?.length || 0);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            console.error('[COUPONS API] Exception fetching coupons:', error);
            return {
                success: false,
                data: [],
                error: error.message,
            };
        }
    },

    /**
     * Validate a coupon code and get discount information
     */
    validateCoupon: async (couponCode: string, totalAmount: number) => {
        try {
            console.log('[COUPONS API] Validating coupon:', couponCode, 'for amount:', totalAmount);

            const payload = {
                coupon_code: couponCode,
                total_amount: totalAmount
            };

            const data = await apiClient.post<CouponValidationResult>('/coupons/validate', payload);

            console.log('[COUPONS API] Coupon validation result:', data);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            console.error('[COUPONS API] Exception validating coupon:', error);
            return {
                success: false,
                data: {
                    valid: false,
                    message: error.message || 'Failed to validate coupon'
                },
                error: error.message,
            };
        }
    }
};

// Bookings API
export const bookingsApi = {
    /**
     * Create a new booking
     */
    createBooking: async (bookingData: {
        userId: string; // Not needed for backend call as it uses token, but kept for interface compat
        courtId: string; // Changed from venueId to courtId
        bookingDate: string;
        startTime: string;
        durationMinutes: number;
        numberOfPlayers?: number;
        pricePerHour?: number; // Selected slot price
        teamName?: string;
        specialRequests?: string;
    }) => {
        try {
            const payload = {
                court_id: bookingData.courtId, // Changed from venue_id to court_id
                booking_date: bookingData.bookingDate,
                start_time: bookingData.startTime,
                duration_minutes: bookingData.durationMinutes,
                number_of_players: bookingData.numberOfPlayers || 2,
                price_per_hour: bookingData.pricePerHour || 200,
                team_name: bookingData.teamName,
                special_requests: bookingData.specialRequests
            };

            const data = await apiClient.post('/bookings/', payload);

            console.log('[BOOKINGS API] Booking created successfully:', data);
            return {
                success: true,
                data: data,
            };
        } catch (error: any) {
            console.error('[BOOKINGS API] Exception creating booking:', error);
            return {
                success: false,
                data: null,
                error: error.message,
            };
        }
    },

    /**
     * Get user's bookings
     */
    getUserBookings: async (userId: string, statusFilter?: string) => {
        try {
            // userId is ignored as backend uses token
            const data = await apiClient.get<any[]>('/bookings/');

            // Filter client-side if needed (or add backend filter)
            let filteredData = data;
            if (statusFilter) {
                filteredData = data.filter(b => b.status === statusFilter);
            }

            console.log('[BOOKINGS API] Fetched user bookings:', filteredData?.length || 0);
            return {
                success: true,
                data: filteredData,
            };
        } catch (error: any) {
            console.error('[BOOKINGS API] Exception fetching bookings:', error);
            return {
                success: false,
                data: [],
                error: error.message,
            };
        }
    },
};
