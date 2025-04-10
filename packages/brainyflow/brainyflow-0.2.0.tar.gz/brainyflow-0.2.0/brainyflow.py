import asyncio, warnings, copy, time

class BaseNode:
    def __init__(self): self.params,self.successors={},{}
    def set_params(self,params): self.params=params
    def add_successor(self,node,action="default"):
        if action in self.successors: warnings.warn(f"Overwriting successor for action '{action}'")
        self.successors[action]=node;return node
    async def prep(self,shared): pass
    async def exec(self,prep_res): pass
    async def post(self,shared,prep_res,exec_res): pass
    async def _exec(self,prep_res): return await self.exec(prep_res)
    async def _run(self,shared): p=await self.prep(shared);e=await self._exec(p);return await self.post(shared,p,e)
    async def run(self,shared): 
        if self.successors: warnings.warn("Node won't run successors. Use Flow!")  
        return await self._run(shared)
    def __rshift__(self,other): return self.add_successor(other)
    def __sub__(self,action):
        if isinstance(action,str): return _ConditionalTransition(self,action)
        raise TypeError("Action must be a string")

class _ConditionalTransition:
    def __init__(self,src,action): self.src,self.action=src,action
    def __rshift__(self,tgt): return self.src.add_successor(tgt,self.action)

class Node(BaseNode):
    def __init__(self,max_retries=1,wait=0): super().__init__();self.max_retries,self.wait=max_retries,wait
    async def exec_fallback(self,prep_res,exc): raise exc
    async def _exec(self,prep_res):
        for self.cur_retry in range(self.max_retries):
            try: return await self.exec(prep_res)
            except Exception as e:
                if self.cur_retry==self.max_retries-1: return await self.exec_fallback(prep_res,e)
                if self.wait>0: await asyncio.sleep(self.wait)

class SequentialBatchNode(Node):
    async def _exec(self,items): return [await super()._exec(i) for i in (items or [])]

class ParallelBatchNode(Node):
    async def _exec(self,items):
        return await asyncio.gather(*[super()._exec(item) for item in items])

class Flow(BaseNode):
    def __init__(self,start): super().__init__();self.start=start
    def get_next_node(self,curr,action):
        nxt=curr.successors.get(action or "default")
        if not nxt and curr.successors: warnings.warn(f"Flow ends: '{action}' not found in {list(curr.successors)}")
        return nxt
    async def _orch(self,shared,params=None):
        curr,p=copy.copy(self.start),(params or {**self.params})
        while curr: curr.set_params(p);c=await curr._run(shared);curr=copy.copy(self.get_next_node(curr,c))
    async def _run(self,shared):pr=await self.prep(shared);await self._orch(shared);return await self.post(shared,pr,None)
    async def exec(self,prep_res): raise RuntimeError("Flow can't exec.")

class SequentialBatchFlow(Flow):
    async def _run(self,shared):
        pr=(await self.prep(shared)) or []
        results = [await self._orch(shared,{**self.params,**bp}) for bp in pr] 
        return await self.post(shared,pr,None)

class ParallelBatchFlow(Flow):
    async def _run(self,shared):
        pr=(await self.prep(shared)) or []
        results = await asyncio.gather(*(self._orch(shared,{**self.params,**bp}) for bp in pr))
        return await self.post(shared,pr,None)
