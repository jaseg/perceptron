#!/usr/bin/env ruby

class Perceptron
    attr_accessor :w

    def initialize(dim, eta)
        @w = Array.new(dim, 1.0/(dim)) #dim+1 ?
        @eta = eta
    end

    def train(d, k, it)
        if test(d) != k.angle
            @w = @w.zip(d).map do |e|
                e[0] + @eta/it*e[1]*k
            end
        end
    end

    def test(d)
        @w.zip(d).inject(0) do |mem, e|
            mem + e[0]*e[1]
        end.angle
    end
    
    def crossvalidate(deg)

    end
end



patterns = File.new("patterns").readlines.reject{|l| l.start_with? "#"}.map{|l| l.split}.reject{|l| l.empty?}.transpose
patterns.each{|l| l.map!{|e| e.to_f}}
labels = File.new("labels").readlines.reject{|l| l.start_with? "#"}.map{|l| l.split}.reject{|l| l.empty?}
labels.each{|l| l.map!{|e| e.to_i}}
if labels.size != 10
    puts "Something went wrong while importing the label data. There are not 10 labels but #{labels.size}. Exiting."
    exit
end
if patterns.size != labels[0].size
    puts "The label count does not match the pattern count. Exiting."
    exit
end
if patterns[0].size != 256
    puts "Something went wrong importing the pattern data. There are not 256 pixels per pattern but #{patterns[0].size}. Exiting."
    exit
end
puts "#Loaded #{patterns.size} patterns."
ps = Array.new()
accuracies = Array.new
#conf = Array.new(10)



eta = 0.5
its = 1000
fold = 10

10.times do|num|
    thisconf = Array.new(10, 0.0)
    accuracy = 0.0
    data = patterns.zip(labels[num]).shuffle.each_slice(patterns.size/fold).to_a
    fold.times do
        p = Perceptron.new(16*16, eta)
        data.rotate!
        train = data[1..fold].flatten(1)
        test = data[0]
        its.times do |it|
            e = train.sample
            p.train(e[0], e[1], it+1)
        end
        test.each do |e|
            if p.test(e[0]) == e[1].angle
                accuracy += 1
            end
        end
        puts "Perceptron weight vector length: #{Math.sqrt(p.w.reduce(0){|m,e|m+e*e})}"
    end
    accuracies << accuracy / patterns.size
    puts "#{num}\t#{accuracies.last}"
    #thisconf.map!{|e|1/patterns.size}
end
