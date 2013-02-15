#!/usr/bin/env python
import random, math, itertools

#patterns = File.new("patterns").readlines.reject{|l| l.start_with? "#"}.map{|l| l.split}.reject{|l| l.empty?}.transpose
#patterns.each{|l| l.map!{|e| e.to_f}}
patterns = list(zip(*[ [float(x) for x in line.split()] for line in open('patterns') if line.strip() and line[0] is not '#' ]))
#labels   = File.new("labels"  ).readlines.reject{|l| l.start_with? "#"}.map{|l| l.split}.reject{|l| l.empty?}
#labels.each{|l| l.map!{|e| e.to_i}}
labels = [ list(map(float, line.split())) for line in open('labels') if line.strip() and line[0] is not '#' ]
if len(labels) != 10:
	raise ValueError('Something went wrong while importing the label data. There are not 10 labels but {}.'.format(len(labels)))
if len(patterns) != len(labels[0]):
	raise ValueError('The label count does not match the pattern count. {} is not {}.'.format(len(patterns), len(labels[0])))
if len(patterns[0]) != 256:
	raise ValueError('Something went wrong importing the pattern data. There are not 256 pixels per pattern but {}.'.format(len(patterns[0])))

eta = 0.5
its = 1000
fold = 10
sg=lambda a:a/abs(a)

per_test=lambda w, s: sum([a*b for a,b in zip(w,s)])
per_train=lambda w, s, k, i: [a+eta/i*b*k for a,b in zip(w, s) if sg(per_test(w, s)) != k]

ps = []
accuracies = []
for num in range(10):
	thisconf = [0.0]*10
	accuracy = 0.0
	#data = patterns.zip(labels[num]).shuffle.each_slice(patterns.size/fold).to_a
	data = list(zip(patterns, labels[num]))
	random.shuffle(data)
	sl = math.ceil(len(patterns)/fold)
	data = [ data[i:i+sl] for i in range(0, len(patterns), sl) ]
	for foo in range(fold):
		n = 16*16
		#p = Perceptron.new(16*16, eta)
		w=[1/n]*n
		data = data[1:] + data[:1]
		train = list(itertools.chain(*data[1:fold]))
		test = data[0]
		for i in range(its):
			#w+=[a+eta/i*b*k for a,b in zip(w,s)] if sg(sum([a*b for a,b in zip(w,s)])) != k/abs(k)
			s, k = random.choice(train)
			w += per_train(w, s, k, i+1)
		accuracy += sum([1 for s, k in test if sg(per_test(w, s)) == k])
		print('Perceptron weight vector length: {}'.format(math.sqrt(sum([ v*v for v in w ]))))
	accuracies.append(accuracy/len(patterns))
	print('{}\t{}'.format(num, accuracies[-1]))

