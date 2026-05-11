import { useQuery, useQueryClient } from '@tanstack/react-query';
import { wisdomService } from '../services/wisdomService';

export function useWisdom() {
  const queryClient = useQueryClient();
  
  const result = useQuery({
    queryKey: ['wisdom', 'today'],
    queryFn: wisdomService.getTodaysWisdom,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 60 * 60 * 1000, // 1 hour
    retry: 3,
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
  
  const refetch = () => {
    queryClient.invalidateQueries({ queryKey: ['wisdom', 'today'] });
  };
  
  return { ...result, refetch };
}
